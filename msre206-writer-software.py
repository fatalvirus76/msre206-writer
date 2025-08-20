import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, Frame, Label, Button, StringVar, IntVar
import serial
import serial.tools.list_ports
import threading
import time
import struct

class MSRE206App:
    def __init__(self, root):
        self.root = root
        self.root.title("MSRE206 Magnetkortsläsare/Skrivare - Komplett")
        self.root.geometry("900x700")
        
        # Serial connection
        self.ser = None
        self.is_connected = False
        
        # Create UI
        self.create_widgets()
        
        # Auto-detect port on startup
        self.auto_detect_port()
    
    def create_widgets(self):
        # Connection frame
        connection_frame = ttk.LabelFrame(self.root, text="Anslutning", padding=10)
        connection_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        ttk.Label(connection_frame, text="Port:").grid(row=0, column=0, sticky="w")
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(connection_frame, textvariable=self.port_var, width=15)
        self.port_combo.grid(row=0, column=1, padx=5)
        
        self.refresh_btn = ttk.Button(connection_frame, text="Uppdatera portar", command=self.refresh_ports)
        self.refresh_btn.grid(row=0, column=2, padx=5)
        
        self.connect_btn = ttk.Button(connection_frame, text="Anslut", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=3, padx=5)
        
        # Status indicator
        self.status_label = ttk.Label(connection_frame, text="Frånkopplad", foreground="red")
        self.status_label.grid(row=0, column=4, padx=10)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        
        # Create tabs
        self.basic_tab = ttk.Frame(self.notebook)
        self.advanced_tab = ttk.Frame(self.notebook)
        self.raw_tab = ttk.Frame(self.notebook)
        self.config_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.basic_tab, text="Grundläggande")
        self.notebook.add(self.advanced_tab, text="Avancerat")
        self.notebook.add(self.raw_tab, text="Rådata")
        self.notebook.add(self.config_tab, text="Konfiguration")
        
        # Setup each tab
        self.setup_basic_tab()
        self.setup_advanced_tab()
        self.setup_raw_tab()
        self.setup_config_tab()
        
        # Log frame
        log_frame = ttk.LabelFrame(self.root, text="Logg", padding=10)
        log_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=85)
        self.log_text.pack(fill="both", expand=True)
        self.log_text.config(state="disabled")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
    
    def setup_basic_tab(self):
        # Track data frame
        data_frame = ttk.LabelFrame(self.basic_tab, text="Kortdata", padding=10)
        data_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Track 1
        ttk.Label(data_frame, text="Spår 1:").grid(row=0, column=0, sticky="w", pady=5)
        self.track1_var = tk.StringVar()
        track1_entry = ttk.Entry(data_frame, textvariable=self.track1_var, width=70)
        track1_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Track 2
        ttk.Label(data_frame, text="Spår 2:").grid(row=1, column=0, sticky="w", pady=5)
        self.track2_var = tk.StringVar()
        track2_entry = ttk.Entry(data_frame, textvariable=self.track2_var, width=70)
        track2_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Track 3
        ttk.Label(data_frame, text="Spår 3:").grid(row=2, column=0, sticky="w", pady=5)
        self.track3_var = tk.StringVar()
        track3_entry = ttk.Entry(data_frame, textvariable=self.track3_var, width=70)
        track3_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        # Track selection for writing
        ttk.Label(data_frame, text="Välj spår att skriva:").grid(row=3, column=0, sticky="w", pady=10)
        
        self.track1_write = tk.BooleanVar(value=True)
        self.track2_write = tk.BooleanVar(value=True)
        self.track3_write = tk.BooleanVar(value=True)
        
        track_select_frame = ttk.Frame(data_frame)
        track_select_frame.grid(row=3, column=1, sticky="w", pady=10)
        
        ttk.Checkbutton(track_select_frame, text="Spår 1", variable=self.track1_write).pack(side="left", padx=5)
        ttk.Checkbutton(track_select_frame, text="Spår 2", variable=self.track2_write).pack(side="left", padx=5)
        ttk.Checkbutton(track_select_frame, text="Spår 3", variable=self.track3_write).pack(side="left", padx=5)
        
        # Buttons frame
        buttons_frame = ttk.Frame(data_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.read_btn = ttk.Button(buttons_frame, text="Läs Kort", command=self.read_card, state="disabled")
        self.read_btn.pack(side="left", padx=5)
        
        self.write_btn = ttk.Button(buttons_frame, text="Skriv Kort", command=self.write_card, state="disabled")
        self.write_btn.pack(side="left", padx=5)
        
        self.erase_btn = ttk.Button(buttons_frame, text="Radera Kort", command=self.erase_card, state="disabled")
        self.erase_btn.pack(side="left", padx=5)
        
        data_frame.columnconfigure(1, weight=1)
    
    def setup_advanced_tab(self):
        # LED Control frame
        led_frame = ttk.LabelFrame(self.advanced_tab, text="LED-kontroll", padding=10)
        led_frame.pack(fill="x", padx=10, pady=5)
        
        led_btn_frame = ttk.Frame(led_frame)
        led_btn_frame.pack(fill="x")
        
        ttk.Button(led_btn_frame, text="Alla LED På", command=lambda: self.led_control(0x82)).pack(side="left", padx=5)
        ttk.Button(led_btn_frame, text="Alla LED Av", command=lambda: self.led_control(0x81)).pack(side="left", padx=5)
        ttk.Button(led_btn_frame, text="Grön LED", command=lambda: self.led_control(0x83)).pack(side="left", padx=5)
        ttk.Button(led_btn_frame, text="Gul LED", command=lambda: self.led_control(0x84)).pack(side="left", padx=5)
        ttk.Button(led_btn_frame, text="Röd LED", command=lambda: self.led_control(0x85)).pack(side="left", padx=5)
        
        # Testing frame
        test_frame = ttk.LabelFrame(self.advanced_tab, text="Testfunktioner", padding=10)
        test_frame.pack(fill="x", padx=10, pady=5)
        
        test_btn_frame = ttk.Frame(test_frame)
        test_btn_frame.pack(fill="x")
        
        ttk.Button(test_btn_frame, text="Kommunikationstest", command=self.communication_test).pack(side="left", padx=5)
        ttk.Button(test_btn_frame, text="Sensortest", command=self.sensor_test).pack(side="left", padx=5)
        ttk.Button(test_btn_frame, text="RAM-test", command=self.ram_test).pack(side="left", padx=5)
        
        # Device Info frame
        info_frame = ttk.LabelFrame(self.advanced_tab, text="Enhetsinformation", padding=10)
        info_frame.pack(fill="x", padx=10, pady=5)
        
        info_btn_frame = ttk.Frame(info_frame)
        info_btn_frame.pack(fill="x")
        
        ttk.Button(info_btn_frame, text="Hämta Modell", command=self.get_device_model).pack(side="left", padx=5)
        ttk.Button(info_btn_frame, text="Hämta Firmware", command=self.get_firmware_version).pack(side="left", padx=5)
        ttk.Button(info_btn_frame, text="Hämta Koercivitetsstatus", command=self.get_coercivity_status).pack(side="left", padx=5)
    
    def setup_raw_tab(self):
        # Raw data frame
        raw_frame = ttk.LabelFrame(self.raw_tab, text="Rådata", padding=10)
        raw_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ttk.Label(raw_frame, text="Spår 1 Rådata:").grid(row=0, column=0, sticky="w", pady=5)
        self.raw_track1_var = tk.StringVar()
        raw_track1_entry = ttk.Entry(raw_frame, textvariable=self.raw_track1_var, width=70)
        raw_track1_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(raw_frame, text="Spår 2 Rådata:").grid(row=1, column=0, sticky="w", pady=5)
        self.raw_track2_var = tk.StringVar()
        raw_track2_entry = ttk.Entry(raw_frame, textvariable=self.raw_track2_var, width=70)
        raw_track2_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(raw_frame, text="Spår 3 Rådata:").grid(row=2, column=0, sticky="w", pady=5)
        self.raw_track3_var = tk.StringVar()
        raw_track3_entry = ttk.Entry(raw_frame, textvariable=self.raw_track3_var, width=70)
        raw_track3_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        # Buttons frame
        raw_btn_frame = ttk.Frame(raw_frame)
        raw_btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(raw_btn_frame, text="Läs Rådata", command=self.read_raw_data).pack(side="left", padx=5)
        ttk.Button(raw_btn_frame, text="Skriv Rådata", command=self.write_raw_data).pack(side="left", padx=5)
        
        raw_frame.columnconfigure(1, weight=1)
    
    def setup_config_tab(self):
        # Configuration frame
        config_frame = ttk.LabelFrame(self.config_tab, text="Konfiguration", padding=10)
        config_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Leading zeros
        ttk.Label(config_frame, text="Ledande nollor (Track 1 & 3):").grid(row=0, column=0, sticky="w", pady=5)
        self.leading_zero_13_var = tk.StringVar(value="61")
        ttk.Entry(config_frame, textvariable=self.leading_zero_13_var, width=10).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(config_frame, text="Ledande nollor (Track 2):").grid(row=1, column=0, sticky="w", pady=5)
        self.leading_zero_2_var = tk.StringVar(value="22")
        ttk.Entry(config_frame, textvariable=self.leading_zero_2_var, width=10).grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Button(config_frame, text="Sätt Ledande Nollor", command=self.set_leading_zeros).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(config_frame, text="Kontrollera Ledande Nollor", command=self.check_leading_zeros).grid(row=3, column=0, columnspan=2, pady=5)
        
        # BPI selection
        ttk.Label(config_frame, text="BPI (Bits Per Inch):").grid(row=4, column=0, sticky="w", pady=5)
        
        bpi_frame = ttk.Frame(config_frame)
        bpi_frame.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        
        self.bpi_track1_var = tk.StringVar(value="210")
        ttk.Label(bpi_frame, text="Track 1:").pack(side="left")
        ttk.Combobox(bpi_frame, textvariable=self.bpi_track1_var, values=["75", "210"], width=5).pack(side="left", padx=5)
        
        self.bpi_track2_var = tk.StringVar(value="210")
        ttk.Label(bpi_frame, text="Track 2:").pack(side="left", padx=(10, 0))
        ttk.Combobox(bpi_frame, textvariable=self.bpi_track2_var, values=["75", "210"], width=5).pack(side="left", padx=5)
        
        self.bpi_track3_var = tk.StringVar(value="210")
        ttk.Label(bpi_frame, text="Track 3:").pack(side="left", padx=(10, 0))
        ttk.Combobox(bpi_frame, textvariable=self.bpi_track3_var, values=["75", "210"], width=5).pack(side="left", padx=5)
        
        ttk.Button(config_frame, text="Sätt BPI", command=self.set_bpi).grid(row=5, column=0, columnspan=2, pady=10)
        
        # BPC selection
        ttk.Label(config_frame, text="BPC (Bits Per Character):").grid(row=6, column=0, sticky="w", pady=5)
        
        bpc_frame = ttk.Frame(config_frame)
        bpc_frame.grid(row=6, column=1, sticky="w", padx=5, pady=5)
        
        self.bpc_track1_var = tk.StringVar(value="7")
        ttk.Label(bpc_frame, text="Track 1:").pack(side="left")
        ttk.Combobox(bpc_frame, textvariable=self.bpc_track1_var, values=["5", "6", "7", "8"], width=3).pack(side="left", padx=5)
        
        self.bpc_track2_var = tk.StringVar(value="5")
        ttk.Label(bpc_frame, text="Track 2:").pack(side="left", padx=(10, 0))
        ttk.Combobox(bpc_frame, textvariable=self.bpc_track2_var, values=["5", "6", "7", "8"], width=3).pack(side="left", padx=5)
        
        self.bpc_track3_var = tk.StringVar(value="5")
        ttk.Label(bpc_frame, text="Track 3:").pack(side="left", padx=(10, 0))
        ttk.Combobox(bpc_frame, textvariable=self.bpc_track3_var, values=["5", "6", "7", "8"], width=3).pack(side="left", padx=5)
        
        ttk.Button(config_frame, text="Sätt BPC", command=self.set_bpc).grid(row=7, column=0, columnspan=2, pady=10)
        
        # Coercivity
        ttk.Label(config_frame, text="Koercivitet:").grid(row=8, column=0, sticky="w", pady=5)
        
        coercivity_frame = ttk.Frame(config_frame)
        coercivity_frame.grid(row=8, column=1, sticky="w", padx=5, pady=5)
        
        self.coercivity_var = tk.StringVar(value="Hi")
        ttk.Radiobutton(coercivity_frame, text="Hög (Hi-Co)", variable=self.coercivity_var, value="Hi").pack(side="left")
        ttk.Radiobutton(coercivity_frame, text="Låg (Low-Co)", variable=self.coercivity_var, value="Low").pack(side="left", padx=(10, 0))
        
        ttk.Button(config_frame, text="Sätt Koercivitet", command=self.set_coercivity).grid(row=9, column=0, columnspan=2, pady=10)
    
    def auto_detect_port(self):
        self.refresh_ports()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "USB" in port.description or "Serial" in port.description:
                self.port_var.set(port.device)
                break
    
    def refresh_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo['values'] = ports
        if ports and not self.port_var.get():
            self.port_var.set(ports[0])
    
    def toggle_connection(self):
        if not self.is_connected:
            self.connect_serial()
        else:
            self.disconnect_serial()
    
    def connect_serial(self):
        port = self.port_var.get()
        if not port:
            messagebox.showerror("Fel", "Vänligen välj en port")
            return
        
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
            self.is_connected = True
            self.connect_btn.config(text="Koppla från")
            self.status_label.config(text="Ansluten", foreground="green")
            self.read_btn.config(state="normal")
            self.write_btn.config(state="normal")
            self.erase_btn.config(state="normal")
            self.log_message(f"Ansluten till {port}")
            
            # Reset device on connect
            self.reset_device()
            
        except Exception as e:
            messagebox.showerror("Anslutningsfel", f"Kunde inte ansluta till {port}:\n{str(e)}")
    
    def disconnect_serial(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.is_connected = False
        self.connect_btn.config(text="Anslut")
        self.status_label.config(text="Frånkopplad", foreground="red")
        self.read_btn.config(state="disabled")
        self.write_btn.config(state="disabled")
        self.erase_btn.config(state="disabled")
        self.log_message("Frånkopplad")
    
    def reset_device(self):
        if self.ser and self.ser.is_open:
            try:
                # Send reset command: <ESC> a
                self.ser.write(bytes([0x1B, 0x61]))
                self.log_message("Enhet återställd")
            except Exception as e:
                self.log_message(f"Fel vid återställning: {str(e)}")
    
    def send_command(self, command, description, expect_response=True, timeout=10):
        if not self.ser or not self.ser.is_open:
            messagebox.showerror("Fel", "Inte ansluten till enheten")
            return None
        
        try:
            self.ser.write(command)
            self.log_message(f"{description} skickad")
            
            if not expect_response:
                return None
                
            # Read response with timeout
            start_time = time.time()
            response = b""
            
            while time.time() - start_time < timeout:
                if self.ser.in_waiting:
                    data = self.ser.read(self.ser.in_waiting)
                    response += data
                    
                    # Check if we have a complete response
                    if len(response) >= 2 and response[-2] == 0x1B:
                        break
                
                time.sleep(0.1)
            
            if response:
                return response
            else:
                self.log_message(f"Timeout: Inget svar på {description}")
                return None
                
        except Exception as e:
            self.log_message(f"Fel vid {description}: {str(e)}")
            return None
    
    def read_card(self):
        response = self.send_command(bytes([0x1B, 0x72]), "Läskommando", timeout=15)
        if response:
            self.process_read_response(response)
    
    def process_read_response(self, response):
        # Response format: <ESC> s <ESC> 1 [data] <ESC> 2 [data] <ESC> 3 [data] ? <FS> <ESC> [status]
        try:
            # Check if response starts with <ESC> s
            if response[0:2] != bytes([0x1B, 0x73]):
                self.log_message("Ogiltigt svar från enheten")
                return
            
            tracks = {1: "", 2: "", 3: ""}
            pos = 2  # Start after <ESC> s
            
            while pos < len(response):
                # Look for track separators
                if pos + 1 < len(response) and response[pos] == 0x1B:
                    track_num = response[pos + 1]
                    pos += 2
                    
                    # Find the end of this track's data (next <ESC> or end marker)
                    end_pos = pos
                    while end_pos < len(response):
                        if response[end_pos] == 0x1B or response[end_pos] == 0x3F:
                            break
                        end_pos += 1
                    
                    # Extract track data
                    if track_num == 0x01:  # Track 1
                        tracks[1] = response[pos:end_pos].decode('ascii', errors='ignore')
                    elif track_num == 0x02:  # Track 2
                        tracks[2] = response[pos:end_pos].decode('ascii', errors='ignore')
                    elif track_num == 0x03:  # Track 3
                        tracks[3] = response[pos:end_pos].decode('ascii', errors='ignore')
                    
                    pos = end_pos
                else:
                    pos += 1
            
            # Update UI with track data
            self.root.after(0, lambda: self.update_track_data(tracks))
            
            # Check status byte (last byte)
            status_byte = response[-1] if len(response) > 0 else None
            if status_byte == 0x30:
                self.log_message("Läsning lyckades")
            else:
                self.log_message(f"Läsningsfel: Statuskod {hex(status_byte)}")
                
        except Exception as e:
            self.log_message(f"Fel vid bearbetning av svar: {str(e)}")
    
    def update_track_data(self, tracks):
        self.track1_var.set(tracks[1])
        self.track2_var.set(tracks[2])
        self.track3_var.set(tracks[3])
    
    def write_card(self):
        # Check if at least one track is selected
        if not any([self.track1_write.get(), self.track2_write.get(), self.track3_write.get()]):
            messagebox.showwarning("Varning", "Välj minst ett spår att skriva till")
            return
        
        # Prepare data block
        data_block = bytes([0x1B, 0x73])  # Start with <ESC> s
        
        # Add track data if selected
        if self.track1_write.get() and self.track1_var.get():
            data_block += bytes([0x1B, 0x01]) + self.track1_var.get().encode('ascii')
        
        if self.track2_write.get() and self.track2_var.get():
            data_block += bytes([0x1B, 0x02]) + self.track2_var.get().encode('ascii')
        
        if self.track3_write.get() and self.track3_var.get():
            data_block += bytes([0x1B, 0x03]) + self.track3_var.get().encode('ascii')
        
        # Add end marker
        data_block += bytes([0x3F, 0x1C])
        
        # Send write command: <ESC> w [data_block]
        response = self.send_command(bytes([0x1B, 0x77]) + data_block, "Skrivkommando", timeout=15)
        
        if response:
            # Response should be <ESC> [status]
            if len(response) >= 2 and response[0] == 0x1B:
                status_byte = response[1]
                if status_byte == 0x30:
                    self.log_message("Skrivning lyckades")
                else:
                    self.log_message(f"Skrivningsfel: Statuskod {hex(status_byte)}")
            else:
                self.log_message("Ogiltigt svar från enheten")
    
    def erase_card(self):
        # Determine which tracks to erase based on selection
        select_byte = 0x00
        if self.track1_write.get():
            select_byte |= 0x01
        if self.track2_write.get():
            select_byte |= 0x02
        if self.track3_write.get():
            select_byte |= 0x04
        
        if select_byte == 0x00:
            messagebox.showwarning("Varning", "Välj minst ett spår att radera")
            return
        
        # Send erase command: <ESC> c [select_byte]
        response = self.send_command(bytes([0x1B, 0x63, select_byte]), "Raderingskommando", timeout=15)
        
        if response:
            # Response should be <ESC> [status]
            if len(response) >= 2 and response[0] == 0x1B:
                status_byte = response[1]
                if status_byte == 0x30:
                    self.log_message("Radering lyckades")
                else:
                    self.log_message(f"Raderingsfel: Statuskod {hex(status_byte)}")
            else:
                self.log_message("Ogiltigt svar från enheten")
    
    def led_control(self, command):
        self.send_command(bytes([0x1B, command]), "LED-kontroll", expect_response=False)
    
    def communication_test(self):
        response = self.send_command(bytes([0x1B, 0x65]), "Kommunikationstest")
        if response and response == bytes([0x1B, 0x79]):
            self.log_message("Kommunikationstest lyckades")
        elif response:
            self.log_message(f"Kommunikationstest misslyckades: {response.hex()}")
    
    def sensor_test(self):
        response = self.send_command(bytes([0x1B, 0x86]), "Sensortest", timeout=30)
        if response and response == bytes([0x1B, 0x30]):
            self.log_message("Sensortest lyckades")
        elif response:
            self.log_message(f"Sensortest misslyckades: {response.hex()}")
    
    def ram_test(self):
        response = self.send_command(bytes([0x1B, 0x87]), "RAM-test")
        if response and response == bytes([0x1B, 0x30]):
            self.log_message("RAM-test lyckades")
        elif response and response == bytes([0x1B, 0x41]):
            self.log_message("RAM-test misslyckades")
        elif response:
            self.log_message(f"RAM-test gav oväntat svar: {response.hex()}")
    
    def get_device_model(self):
        response = self.send_command(bytes([0x1B, 0x74]), "Hämta modell")
        if response and len(response) >= 3 and response[0] == 0x1B and response[-1] == 0x53:
            model = response[1:-1].decode('ascii', errors='ignore')
            self.log_message(f"Enhetsmodell: {model}")
        elif response:
            self.log_message(f"Kunde inte hämta modell: {response.hex()}")
    
    def get_firmware_version(self):
        response = self.send_command(bytes([0x1B, 0x76]), "Hämta firmware")
        if response and response[0] == 0x1B:
            version = response[1:].decode('ascii', errors='ignore')
            self.log_message(f"Firmware-version: {version}")
        elif response:
            self.log_message(f"Kunde inte hämta firmware: {response.hex()}")
    
    def get_coercivity_status(self):
        response = self.send_command(bytes([0x1B, 0x64]), "Hämta koercivitetsstatus")
        if response and response == bytes([0x1B, 0x48]):
            self.log_message("Koercivitetsstatus: Hög (Hi-Co)")
        elif response and response == bytes([0x1B, 0x4C]):
            self.log_message("Koercivitetsstatus: Låg (Low-Co)")
        elif response:
            self.log_message(f"Kunde inte hämta koercivitetsstatus: {response.hex()}")
    
    def read_raw_data(self):
        response = self.send_command(bytes([0x1B, 0x6D]), "Läs rådata", timeout=15)
        if response:
            self.process_raw_read_response(response)
    
    def process_raw_read_response(self, response):
        # Response format: <ESC> s <ESC> 1 [L1] [data] <ESC> 2 [L2] [data] <ESC> 3 [L3] [data] ? <FS> <ESC> [status]
        try:
            # Check if response starts with <ESC> s
            if response[0:2] != bytes([0x1B, 0x73]):
                self.log_message("Ogiltigt svar från enheten")
                return
            
            tracks = {1: "", 2: "", 3: ""}
            pos = 2  # Start after <ESC> s
            
            while pos < len(response):
                # Look for track separators
                if pos + 1 < len(response) and response[pos] == 0x1B:
                    track_num = response[pos + 1]
                    pos += 2
                    
                    if pos >= len(response):
                        break
                    
                    # Get length byte
                    length = response[pos]
                    pos += 1
                    
                    # Extract track data
                    if pos + length <= len(response):
                        data = response[pos:pos+length]
                        if track_num == 0x01:  # Track 1
                            tracks[1] = data.hex()
                        elif track_num == 0x02:  # Track 2
                            tracks[2] = data.hex()
                        elif track_num == 0x03:  # Track 3
                            tracks[3] = data.hex()
                        
                        pos += length
                    else:
                        break
                else:
                    pos += 1
            
            # Update UI with raw track data
            self.root.after(0, lambda: self.update_raw_track_data(tracks))
            
            # Check status byte (last byte)
            status_byte = response[-1] if len(response) > 0 else None
            if status_byte == 0x30:
                self.log_message("Rådataläsning lyckades")
            else:
                self.log_message(f"Rådataläsningsfel: Statuskod {hex(status_byte)}")
                
        except Exception as e:
            self.log_message(f"Fel vid bearbetning av rådatasvar: {str(e)}")
    
    def update_raw_track_data(self, tracks):
        self.raw_track1_var.set(tracks[1])
        self.raw_track2_var.set(tracks[2])
        self.raw_track3_var.set(tracks[3])
    
    def write_raw_data(self):
        # Prepare raw data block
        data_block = bytes([0x1B, 0x73])  # Start with <ESC> s
        
        # Add track 1 raw data if available
        if self.raw_track1_var.get():
            try:
                raw_data = bytes.fromhex(self.raw_track1_var.get())
                data_block += bytes([0x1B, 0x01, len(raw_data)]) + raw_data
            except ValueError:
                self.log_message("Ogiltigt hexadecimalt format för spår 1")
                return
        
        # Add track 2 raw data if available
        if self.raw_track2_var.get():
            try:
                raw_data = bytes.fromhex(self.raw_track2_var.get())
                data_block += bytes([0x1B, 0x02, len(raw_data)]) + raw_data
            except ValueError:
                self.log_message("Ogiltigt hexadecimalt format för spår 2")
                return
        
        # Add track 3 raw data if available
        if self.raw_track3_var.get():
            try:
                raw_data = bytes.fromhex(self.raw_track3_var.get())
                data_block += bytes([0x1B, 0x03, len(raw_data)]) + raw_data
            except ValueError:
                self.log_message("Ogiltigt hexadecimalt format för spår 3")
                return
        
        # Add end marker
        data_block += bytes([0x3F, 0x1C])
        
        # Send write raw command: <ESC> n [data_block]
        response = self.send_command(bytes([0x1B, 0x6E]) + data_block, "Skriv rådatakommando", timeout=15)
        
        if response:
            # Response should be <ESC> [status]
            if len(response) >= 2 and response[0] == 0x1B:
                status_byte = response[1]
                if status_byte == 0x30:
                    self.log_message("Rådataskrivning lyckades")
                else:
                    self.log_message(f"Rådataskrivningsfel: Statuskod {hex(status_byte)}")
            else:
                self.log_message("Ogiltigt svar från enheten")
    
    def set_leading_zeros(self):
        try:
            lz_13 = int(self.leading_zero_13_var.get())
            lz_2 = int(self.leading_zero_2_var.get())
            
            if not (0 <= lz_13 <= 255) or not (0 <= lz_2 <= 255):
                raise ValueError("Värden måste vara mellan 0 och 255")
            
            response = self.send_command(bytes([0x1B, 0x7A, lz_13, lz_2]), "Sätt ledande nollor")
            
            if response and response == bytes([0x1B, 0x30]):
                self.log_message("Ledande nollor inställda")
            elif response and response == bytes([0x1B, 0x41]):
                self.log_message("Misslyckades att sätta ledande nollor")
            elif response:
                self.log_message(f"Oväntat svar på sätt ledande nollor: {response.hex()}")
                
        except ValueError as e:
            self.log_message(f"Ogiltigt värde för ledande nollor: {str(e)}")
    
    def check_leading_zeros(self):
        response = self.send_command(bytes([0x1B, 0x6C]), "Kontrollera ledande nollor")
        
        if response and len(response) == 3 and response[0] == 0x1B:
            lz_13 = response[1]
            lz_2 = response[2]
            self.log_message(f"Ledande nollor - Spår 1&3: {lz_13}, Spår 2: {lz_2}")
        elif response:
            self.log_message(f"Kunde inte kontrollera ledande nollor: {response.hex()}")
    
    def set_bpi(self):
        try:
            # Track 1 BPI
            if self.bpi_track1_var.get() == "210":
                bpi_t1_cmd = bytes([0x1B, 0x62, 0xA1])
            else:
                bpi_t1_cmd = bytes([0x1B, 0x62, 0xA0])
            
            # Track 2 BPI
            if self.bpi_track2_var.get() == "210":
                bpi_t2_cmd = bytes([0x1B, 0x62, 0xD2])
            else:
                bpi_t2_cmd = bytes([0x1B, 0x62, 0x4B])
            
            # Track 3 BPI
            if self.bpi_track3_var.get() == "210":
                bpi_t3_cmd = bytes([0x1B, 0x62, 0xC1])
            else:
                bpi_t3_cmd = bytes([0x1B, 0x62, 0xC0])
            
            # Send commands
            for cmd, track in [(bpi_t1_cmd, "Spår 1"), (bpi_t2_cmd, "Spår 2"), (bpi_t3_cmd, "Spår 3")]:
                response = self.send_command(cmd, f"Sätt BPI för {track}")
                if response and response == bytes([0x1B, 0x30]):
                    self.log_message(f"BPI för {track} inställd till {self.bpi_track1_var.get() if track == 'Spår 1' else self.bpi_track2_var.get() if track == 'Spår 2' else self.bpi_track3_var.get()} bpi")
                elif response:
                    self.log_message(f"Misslyckades att sätta BPI för {track}: {response.hex()}")
                    
        except Exception as e:
            self.log_message(f"Fel vid inställning av BPI: {str(e)}")
    
    def set_bpc(self):
        try:
            bpc_t1 = int(self.bpc_track1_var.get())
            bpc_t2 = int(self.bpc_track2_var.get())
            bpc_t3 = int(self.bpc_track3_var.get())
            
            if not (5 <= bpc_t1 <= 8) or not (5 <= bpc_t2 <= 8) or not (5 <= bpc_t3 <= 8):
                raise ValueError("BPC-värden måste vara mellan 5 och 8")
            
            response = self.send_command(bytes([0x1B, 0x6F, bpc_t1, bpc_t2, bpc_t3]), "Sätt BPC")
            
            if response and len(response) == 5 and response[0] == 0x1B and response[1] == 0x30:
                self.log_message(f"BPC inställd - Spår 1: {response[2]}, Spår 2: {response[3]}, Spår 3: {response[4]}")
            elif response:
                self.log_message(f"Kunde inte sätta BPC: {response.hex()}")
                
        except ValueError as e:
            self.log_message(f"Ogiltigt värde för BPC: {str(e)}")
    
    def set_coercivity(self):
        if self.coercivity_var.get() == "Hi":
            response = self.send_command(bytes([0x1B, 0x78]), "Sätt hög koercivitet")
        else:
            response = self.send_command(bytes([0x1B, 0x79]), "Sätt låg koercivitet")
        
        if response and response == bytes([0x1B, 0x30]):
            self.log_message(f"Koercivitet inställd till {'Hög (Hi-Co)' if self.coercivity_var.get() == 'Hi' else 'Låg (Low-Co)'}")
        elif response:
            self.log_message(f"Kunde inte sätta koercivitet: {response.hex()}")
    
    def log_message(self, message):
        def update_log():
            self.log_text.config(state="normal")
            self.log_text.insert("end", f"{time.strftime('%H:%M:%S')} - {message}\n")
            self.log_text.see("end")
            self.log_text.config(state="disabled")
        
        self.root.after(0, update_log)

if __name__ == "__main__":
    root = tk.Tk()
    app = MSRE206App(root)
    root.mainloop()
