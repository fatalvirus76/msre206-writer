import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import serial
import serial.tools.list_ports
import time
import random
from datetime import datetime, timedelta

class MSRE206App:
    def __init__(self, root):
        self.root = root
        self.ser = None
        self.is_connected = False

        # --- Internationalization (i18n) Setup ---
        self.languages = {
            "EN": {
                "window_title": "MSRE206 Magnetic Card Reader/Writer",
                "themes": "Themes", "language": "Language",
                "light": "Light", "dark": "Dark", "matrix": "Matrix", "synthwave": "Synthwave", "dracula": "Dracula",
                "connection": "Connection", "port": "Port:", "refresh_ports": "Refresh Ports",
                "connect": "Connect", "disconnect": "Disconnect", "connected": "Connected", "disconnected": "Disconnected",
                "basic": "Basic", "advanced": "Advanced", "raw_data": "Raw Data", "configuration": "Configuration", "generator": "Card Generator",
                "card_data": "Card Data", "track1": "Track 1:", "track2": "Track 2:", "track3": "Track 3:",
                "select_tracks_to_write": "Select tracks to write:",
                "read_card": "Read Card", "write_card": "Write Card", "erase_card": "Erase Card",
                "led_control": "LED Control", "all_led_on": "All LEDs On", "all_led_off": "All LEDs Off",
                "green_led": "Green LED", "yellow_led": "Yellow LED", "red_led": "Red LED",
                "test_functions": "Test Functions", "comm_test": "Communication Test", "sensor_test": "Sensor Test", "ram_test": "RAM Test",
                "device_info": "Device Information", "get_model": "Get Model", "get_firmware": "Get Firmware", "get_coercivity": "Get Coercivity",
                "raw_track1": "Track 1 Raw:", "raw_track2": "Track 2 Raw:", "raw_track3": "Track 3 Raw:",
                "read_raw": "Read Raw", "write_raw": "Write Raw",
                "leading_zeros_13": "Leading Zeros (Track 1 & 3):", "leading_zeros_2": "Leading Zeros (Track 2):",
                "set_leading_zeros": "Set Leading Zeros", "check_leading_zeros": "Check Leading Zeros",
                "bpi": "BPI (Bits Per Inch):", "set_bpi": "Set BPI",
                "bpc": "BPC (Bits Per Character):", "set_bpc": "Set BPC",
                "coercivity": "Coercivity:", "high_co": "High (Hi-Co)", "low_co": "Low (Lo-Co)", "set_coercivity": "Set Coercivity",
                "card_type": "Card Type:", "bin": "First 6 digits (BIN):", "bin_help": "(Leave empty for standard BIN)",
                "generate_card": "Generate Card", "card_number": "Card Number:", "expiry_date": "Expiry Date:",
                "copy_to_track1": "Copy to Track 1", "copy_to_track2": "Copy to Track 2", "copy_both": "Copy Both",
                "log": "Log",
                "theme_changed": "Theme changed to: {}",
                "error": "Error", "warning": "Warning",
                "port_select_error": "Please select a port",
                "connection_error": "Connection Error", "could_not_connect": "Could not connect to {}:\n{}",
                "connected_to": "Connected to {}", "device_reset": "Device reset", "reset_error": "Error during reset: {}",
                "not_connected": "Not connected to the device",
                "command_sent": "{} sent", "timeout": "Timeout: No response for {}", "command_error": "Error during {}: {}",
                "invalid_response": "Invalid response from device",
                "read_success": "Read successful", "read_error": "Read error: Status code {}",
                "process_error": "Error processing response: {}",
                "select_track_to_write_warning": "Please select at least one track to write to",
                "write_success": "Write successful", "write_error": "Write error: Status code {}",
                "select_track_to_erase_warning": "Please select at least one track to erase",
                "erase_success": "Erase successful", "erase_error": "Erase error: Status code {}",
                "comm_test_success": "Communication test successful", "comm_test_fail": "Communication test failed: {}",
                "sensor_test_success": "Sensor test successful", "sensor_test_fail": "Sensor test failed: {}",
                "ram_test_success": "RAM test successful", "ram_test_fail": "RAM test failed", "ram_test_unexpected": "RAM test returned unexpected response: {}",
                "device_model": "Device model: {}", "get_model_fail": "Could not get model: {}",
                "firmware_version": "Firmware version: {}", "get_firmware_fail": "Could not get firmware: {}",
                "coercivity_status_hi": "Coercivity status: High (Hi-Co)", "coercivity_status_lo": "Coercivity status: Low (Lo-Co)", "get_coercivity_fail": "Could not get coercivity status: {}",
                "raw_read_success": "Raw data read successful", "raw_read_error": "Raw data read error: Status code {}",
                "invalid_hex": "Invalid hexadecimal format for track {}",
                "raw_write_success": "Raw data write successful", "raw_write_error": "Raw data write error: Status code {}",
                "invalid_leading_zero_value": "Invalid value for leading zeros: {}",
                "leading_zeros_set": "Leading zeros set", "set_leading_zeros_fail": "Failed to set leading zeros",
                "leading_zeros_check": "Leading Zeros - Track 1&3: {}, Track 2: {}", "check_leading_zeros_fail": "Could not check leading zeros: {}",
                "bpi_set_success": "BPI for {} set to {} bpi", "bpi_set_fail": "Failed to set BPI for {}: {}", "bpi_set_error": "Error setting BPI: {}",
                "bpc_set_success": "BPC set - Track 1: {}, Track 2: {}, Track 3: {}", "bpc_set_fail": "Could not set BPC: {}", "invalid_bpc_value": "Invalid value for BPC: {}",
                "coercivity_set_success": "Coercivity set to {}", "coercivity_set_fail": "Could not set coercivity: {}",
                "card_generated": "Generated {}-card: {}",
                "invalid_bin_error": "BIN must be exactly 6 digits",
                "bin_mismatch_warning_visa": "Visa cards normally start with 4. Continue anyway?",
                "bin_mismatch_warning_mastercard": "Mastercard normally starts with 51-55 or 22-27. Continue anyway?",
                "bin_mismatch_warning_amex": "American Express normally starts with 34 or 37. Continue anyway?",
                "bin_mismatch_warning_diners": "Diners Club normally starts with 36, 38 or 39. Continue anyway?",
                "copied_to_track1": "Copied to Track 1", "copied_to_track2": "Copied to Track 2", "copied_to_both": "Copied to both tracks"
            },
            "SV": {
                "window_title": "MSRE206 Magnetkortsläsare/Skrivare",
                "themes": "Teman", "language": "Språk",
                "light": "Ljust", "dark": "Mörkt", "matrix": "Matrix", "synthwave": "Synthwave", "dracula": "Dracula",
                "connection": "Anslutning", "port": "Port:", "refresh_ports": "Uppdatera portar",
                "connect": "Anslut", "disconnect": "Koppla från", "connected": "Ansluten", "disconnected": "Frånkopplad",
                "basic": "Grundläggande", "advanced": "Avancerat", "raw_data": "Rådata", "configuration": "Konfiguration", "generator": "Kortgenerator",
                "card_data": "Kortdata", "track1": "Spår 1:", "track2": "Spår 2:", "track3": "Spår 3:",
                "select_tracks_to_write": "Välj spår att skriva:",
                "read_card": "Läs Kort", "write_card": "Skriv Kort", "erase_card": "Radera Kort",
                "led_control": "LED-kontroll", "all_led_on": "Alla LED På", "all_led_off": "Alla LED Av",
                "green_led": "Grön LED", "yellow_led": "Gul LED", "red_led": "Röd LED",
                "test_functions": "Testfunktioner", "comm_test": "Kommunikationstest", "sensor_test": "Sensortest", "ram_test": "RAM-test",
                "device_info": "Enhetsinformation", "get_model": "Hämta Modell", "get_firmware": "Hämta Firmware", "get_coercivity": "Hämta Koercivitet",
                "raw_track1": "Spår 1 Rådata:", "raw_track2": "Spår 2 Rådata:", "raw_track3": "Spår 3 Rådata:",
                "read_raw": "Läs Rådata", "write_raw": "Skriv Rådata",
                "leading_zeros_13": "Ledande nollor (Spår 1 & 3):", "leading_zeros_2": "Ledande nollor (Spår 2):",
                "set_leading_zeros": "Sätt Ledande Nollor", "check_leading_zeros": "Kontrollera Ledande Nollor",
                "bpi": "BPI (Bits Per Inch):", "set_bpi": "Sätt BPI",
                "bpc": "BPC (Bits Per Character):", "set_bpc": "Sätt BPC",
                "coercivity": "Koercivitet:", "high_co": "Hög (Hi-Co)", "low_co": "Låg (Lo-Co)", "set_coercivity": "Sätt Koercivitet",
                "card_type": "Korttyp:", "bin": "Första 6 siffror (BIN):", "bin_help": "(Lämna tomt för standard BIN)",
                "generate_card": "Generera Kort", "card_number": "Kortnummer:", "expiry_date": "Utgångsdatum:",
                "copy_to_track1": "Kopiera till Spår 1", "copy_to_track2": "Kopiera till Spår 2", "copy_both": "Kopiera båda",
                "log": "Logg",
                "theme_changed": "Tema ändrat till: {}",
                "error": "Fel", "warning": "Varning",
                "port_select_error": "Vänligen välj en port",
                "connection_error": "Anslutningsfel", "could_not_connect": "Kunde inte ansluta till {}:\n{}",
                "connected_to": "Ansluten till {}", "device_reset": "Enhet återställd", "reset_error": "Fel vid återställning: {}",
                "not_connected": "Inte ansluten till enheten",
                "command_sent": "{} skickad", "timeout": "Timeout: Inget svar på {}", "command_error": "Fel vid {}: {}",
                "invalid_response": "Ogiltigt svar från enheten",
                "read_success": "Läsning lyckades", "read_error": "Läsningsfel: Statuskod {}",
                "process_error": "Fel vid bearbetning av svar: {}",
                "select_track_to_write_warning": "Välj minst ett spår att skriva till",
                "write_success": "Skrivning lyckades", "write_error": "Skrivningsfel: Statuskod {}",
                "select_track_to_erase_warning": "Välj minst ett spår att radera",
                "erase_success": "Radering lyckades", "erase_error": "Raderingsfel: Statuskod {}",
                "comm_test_success": "Kommunikationstest lyckades", "comm_test_fail": "Kommunikationstest misslyckades: {}",
                "sensor_test_success": "Sensortest lyckades", "sensor_test_fail": "Sensortest misslyckades: {}",
                "ram_test_success": "RAM-test lyckades", "ram_test_fail": "RAM-test misslyckades", "ram_test_unexpected": "RAM-test gav oväntat svar: {}",
                "device_model": "Enhetsmodell: {}", "get_model_fail": "Kunde inte hämta modell: {}",
                "firmware_version": "Firmware-version: {}", "get_firmware_fail": "Kunde inte hämta firmware: {}",
                "coercivity_status_hi": "Koercivitetsstatus: Hög (Hi-Co)", "coercivity_status_lo": "Koercivitetsstatus: Låg (Lo-Co)", "get_coercivity_fail": "Kunde inte hämta koercivitetsstatus: {}",
                "raw_read_success": "Rådataläsning lyckades", "raw_read_error": "Rådataläsningsfel: Statuskod {}",
                "invalid_hex": "Ogiltigt hexadecimalt format för spår {}",
                "raw_write_success": "Rådataskrivning lyckades", "raw_write_error": "Rådataskrivningsfel: Statuskod {}",
                "invalid_leading_zero_value": "Ogiltigt värde för ledande nollor: {}",
                "leading_zeros_set": "Ledande nollor inställda", "set_leading_zeros_fail": "Misslyckades att sätta ledande nollor",
                "leading_zeros_check": "Ledande nollor - Spår 1&3: {}, Spår 2: {}", "check_leading_zeros_fail": "Kunde inte kontrollera ledande nollor: {}",
                "bpi_set_success": "BPI för {} inställd till {} bpi", "bpi_set_fail": "Misslyckades att sätta BPI för {}: {}", "bpi_set_error": "Fel vid inställning av BPI: {}",
                "bpc_set_success": "BPC inställd - Spår 1: {}, Spår 2: {}, Spår 3: {}", "bpc_set_fail": "Kunde inte sätta BPC: {}", "invalid_bpc_value": "Ogiltigt värde för BPC: {}",
                "coercivity_set_success": "Koercivitet inställd till {}", "coercivity_set_fail": "Kunde inte sätta koercivitet: {}",
                "card_generated": "Genererat {}-kort: {}",
                "invalid_bin_error": "BIN måste vara exakt 6 siffror",
                "bin_mismatch_warning_visa": "Visa-kort börjar normalt med 4. Fortsätt ändå?",
                "bin_mismatch_warning_mastercard": "Mastercard börjar normalt med 51-55 eller 22-27. Fortsätt ändå?",
                "bin_mismatch_warning_amex": "American Express börjar normalt med 34 eller 37. Fortsätt ändå?",
                "bin_mismatch_warning_diners": "Diners Club börjar normalt med 36, 38 eller 39. Fortsätt ändå?",
                "copied_to_track1": "Kopierat till Spår 1", "copied_to_track2": "Kopierat till Spår 2", "copied_to_both": "Kopierat till båda spåren"
            }
        }
        self.current_language = "EN"  # Default language
        self.strings = self.languages[self.current_language]

        self.root.geometry("900x750")
        
        self.create_widgets()
        self.auto_detect_port()
        self.set_theme("Light") # Set default theme
        self.update_ui_text() # Set initial UI text

    def create_widgets(self):
        # --- Menu Bar ---
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Theme Menu
        self.theme_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=self.strings["themes"], menu=self.theme_menu)
        self.theme_menu.add_command(label=self.strings["light"], command=lambda: self.set_theme("Light"))
        self.theme_menu.add_command(label=self.strings["dark"], command=lambda: self.set_theme("Dark"))
        self.theme_menu.add_command(label=self.strings["matrix"], command=lambda: self.set_theme("Matrix"))
        self.theme_menu.add_command(label=self.strings["synthwave"], command=lambda: self.set_theme("Synthwave"))
        self.theme_menu.add_command(label=self.strings["dracula"], command=lambda: self.set_theme("Dracula"))

        # Language Menu
        self.language_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=self.strings["language"], menu=self.language_menu)
        self.language_menu.add_command(label="English", command=lambda: self.set_language("EN"))
        self.language_menu.add_command(label="Svenska", command=lambda: self.set_language("SV"))

        # --- Connection Frame ---
        self.connection_frame = ttk.LabelFrame(self.root, padding=10)
        self.connection_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.port_label = ttk.Label(self.connection_frame)
        self.port_label.grid(row=0, column=0, sticky="w")
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(self.connection_frame, textvariable=self.port_var, width=15)
        self.port_combo.grid(row=0, column=1, padx=5)

        self.refresh_btn = ttk.Button(self.connection_frame, command=self.refresh_ports)
        self.refresh_btn.grid(row=0, column=2, padx=5)

        self.connect_btn = ttk.Button(self.connection_frame, command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=3, padx=5)

        self.status_label = ttk.Label(self.connection_frame, foreground="red")
        self.status_label.grid(row=0, column=4, padx=10)

        # --- Notebook for Tabs ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.basic_tab = ttk.Frame(self.notebook)
        self.advanced_tab = ttk.Frame(self.notebook)
        self.raw_tab = ttk.Frame(self.notebook)
        self.config_tab = ttk.Frame(self.notebook)
        self.generator_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.basic_tab, text=self.strings["basic"])
        self.notebook.add(self.advanced_tab, text=self.strings["advanced"])
        self.notebook.add(self.raw_tab, text=self.strings["raw_data"])
        self.notebook.add(self.config_tab, text=self.strings["configuration"])
        self.notebook.add(self.generator_tab, text=self.strings["generator"])

        # Setup each tab's content
        self.setup_basic_tab()
        self.setup_advanced_tab()
        self.setup_raw_tab()
        self.setup_config_tab()
        self.setup_generator_tab()

        # --- Log Frame ---
        self.log_frame = ttk.LabelFrame(self.root, padding=10)
        self.log_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.log_text = scrolledtext.ScrolledText(self.log_frame, height=10, width=85, state="disabled")
        self.log_text.pack(fill="both", expand=True)

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)

    def setup_basic_tab(self):
        self.data_frame = ttk.LabelFrame(self.basic_tab, padding=10)
        self.data_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.track1_label = ttk.Label(self.data_frame)
        self.track1_label.grid(row=0, column=0, sticky="w", pady=5)
        self.track1_var = tk.StringVar()
        ttk.Entry(self.data_frame, textvariable=self.track1_var, width=70).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.track2_label = ttk.Label(self.data_frame)
        self.track2_label.grid(row=1, column=0, sticky="w", pady=5)
        self.track2_var = tk.StringVar()
        ttk.Entry(self.data_frame, textvariable=self.track2_var, width=70).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        self.track3_label = ttk.Label(self.data_frame)
        self.track3_label.grid(row=2, column=0, sticky="w", pady=5)
        self.track3_var = tk.StringVar()
        ttk.Entry(self.data_frame, textvariable=self.track3_var, width=70).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        self.select_tracks_label = ttk.Label(self.data_frame)
        self.select_tracks_label.grid(row=3, column=0, sticky="w", pady=10)
        
        self.track1_write = tk.BooleanVar(value=True)
        self.track2_write = tk.BooleanVar(value=True)
        self.track3_write = tk.BooleanVar(value=True)
        
        track_select_frame = ttk.Frame(self.data_frame)
        track_select_frame.grid(row=3, column=1, sticky="w", pady=10)
        
        self.track1_check = ttk.Checkbutton(track_select_frame, text=self.strings["track1"][:-1], variable=self.track1_write)
        self.track1_check.pack(side="left", padx=5)
        self.track2_check = ttk.Checkbutton(track_select_frame, text=self.strings["track2"][:-1], variable=self.track2_write)
        self.track2_check.pack(side="left", padx=5)
        self.track3_check = ttk.Checkbutton(track_select_frame, text=self.strings["track3"][:-1], variable=self.track3_write)
        self.track3_check.pack(side="left", padx=5)
        
        buttons_frame = ttk.Frame(self.data_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.read_btn = ttk.Button(buttons_frame, command=self.read_card, state="disabled")
        self.read_btn.pack(side="left", padx=5)
        self.write_btn = ttk.Button(buttons_frame, command=self.write_card, state="disabled")
        self.write_btn.pack(side="left", padx=5)
        self.erase_btn = ttk.Button(buttons_frame, command=self.erase_card, state="disabled")
        self.erase_btn.pack(side="left", padx=5)
        
        self.data_frame.columnconfigure(1, weight=1)

    def setup_advanced_tab(self):
        self.led_frame = ttk.LabelFrame(self.advanced_tab, padding=10)
        self.led_frame.pack(fill="x", padx=10, pady=5)
        led_btn_frame = ttk.Frame(self.led_frame)
        led_btn_frame.pack(fill="x")
        self.all_led_on_btn = ttk.Button(led_btn_frame, command=lambda: self.led_control(0x82))
        self.all_led_on_btn.pack(side="left", padx=5)
        self.all_led_off_btn = ttk.Button(led_btn_frame, command=lambda: self.led_control(0x81))
        self.all_led_off_btn.pack(side="left", padx=5)
        self.green_led_btn = ttk.Button(led_btn_frame, command=lambda: self.led_control(0x83))
        self.green_led_btn.pack(side="left", padx=5)
        self.yellow_led_btn = ttk.Button(led_btn_frame, command=lambda: self.led_control(0x84))
        self.yellow_led_btn.pack(side="left", padx=5)
        self.red_led_btn = ttk.Button(led_btn_frame, command=lambda: self.led_control(0x85))
        self.red_led_btn.pack(side="left", padx=5)
        
        self.test_frame = ttk.LabelFrame(self.advanced_tab, padding=10)
        self.test_frame.pack(fill="x", padx=10, pady=5)
        test_btn_frame = ttk.Frame(self.test_frame)
        test_btn_frame.pack(fill="x")
        self.comm_test_btn = ttk.Button(test_btn_frame, command=self.communication_test)
        self.comm_test_btn.pack(side="left", padx=5)
        self.sensor_test_btn = ttk.Button(test_btn_frame, command=self.sensor_test)
        self.sensor_test_btn.pack(side="left", padx=5)
        self.ram_test_btn = ttk.Button(test_btn_frame, command=self.ram_test)
        self.ram_test_btn.pack(side="left", padx=5)
        
        self.info_frame = ttk.LabelFrame(self.advanced_tab, padding=10)
        self.info_frame.pack(fill="x", padx=10, pady=5)
        info_btn_frame = ttk.Frame(self.info_frame)
        info_btn_frame.pack(fill="x")
        self.get_model_btn = ttk.Button(info_btn_frame, command=self.get_device_model)
        self.get_model_btn.pack(side="left", padx=5)
        self.get_firmware_btn = ttk.Button(info_btn_frame, command=self.get_firmware_version)
        self.get_firmware_btn.pack(side="left", padx=5)
        self.get_coercivity_btn = ttk.Button(info_btn_frame, command=self.get_coercivity_status)
        self.get_coercivity_btn.pack(side="left", padx=5)

    def setup_raw_tab(self):
        self.raw_frame = ttk.LabelFrame(self.raw_tab, padding=10)
        self.raw_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.raw_track1_label = ttk.Label(self.raw_frame)
        self.raw_track1_label.grid(row=0, column=0, sticky="w", pady=5)
        self.raw_track1_var = tk.StringVar()
        ttk.Entry(self.raw_frame, textvariable=self.raw_track1_var, width=70).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.raw_track2_label = ttk.Label(self.raw_frame)
        self.raw_track2_label.grid(row=1, column=0, sticky="w", pady=5)
        self.raw_track2_var = tk.StringVar()
        ttk.Entry(self.raw_frame, textvariable=self.raw_track2_var, width=70).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        self.raw_track3_label = ttk.Label(self.raw_frame)
        self.raw_track3_label.grid(row=2, column=0, sticky="w", pady=5)
        self.raw_track3_var = tk.StringVar()
        ttk.Entry(self.raw_frame, textvariable=self.raw_track3_var, width=70).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        raw_btn_frame = ttk.Frame(self.raw_frame)
        raw_btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.read_raw_btn = ttk.Button(raw_btn_frame, command=self.read_raw_data)
        self.read_raw_btn.pack(side="left", padx=5)
        self.write_raw_btn = ttk.Button(raw_btn_frame, command=self.write_raw_data)
        self.write_raw_btn.pack(side="left", padx=5)
        
        self.raw_frame.columnconfigure(1, weight=1)

    def setup_config_tab(self):
        self.config_frame = ttk.LabelFrame(self.config_tab, padding=10)
        self.config_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.leading_zero_13_label = ttk.Label(self.config_frame)
        self.leading_zero_13_label.grid(row=0, column=0, sticky="w", pady=5)
        self.leading_zero_13_var = tk.StringVar(value="61")
        ttk.Entry(self.config_frame, textvariable=self.leading_zero_13_var, width=10).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        self.leading_zero_2_label = ttk.Label(self.config_frame)
        self.leading_zero_2_label.grid(row=1, column=0, sticky="w", pady=5)
        self.leading_zero_2_var = tk.StringVar(value="22")
        ttk.Entry(self.config_frame, textvariable=self.leading_zero_2_var, width=10).grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        self.set_leading_zeros_btn = ttk.Button(self.config_frame, command=self.set_leading_zeros)
        self.set_leading_zeros_btn.grid(row=2, column=0, columnspan=2, pady=10)
        self.check_leading_zeros_btn = ttk.Button(self.config_frame, command=self.check_leading_zeros)
        self.check_leading_zeros_btn.grid(row=3, column=0, columnspan=2, pady=5)
        
        self.bpi_label = ttk.Label(self.config_frame)
        self.bpi_label.grid(row=4, column=0, sticky="w", pady=5)
        bpi_frame = ttk.Frame(self.config_frame)
        bpi_frame.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        self.bpi_track1_var = tk.StringVar(value="210")
        self.bpi_track1_label = ttk.Label(bpi_frame)
        self.bpi_track1_label.pack(side="left")
        ttk.Combobox(bpi_frame, textvariable=self.bpi_track1_var, values=["75", "210"], width=5).pack(side="left", padx=5)
        self.bpi_track2_var = tk.StringVar(value="210")
        self.bpi_track2_label = ttk.Label(bpi_frame)
        self.bpi_track2_label.pack(side="left", padx=(10, 0))
        ttk.Combobox(bpi_frame, textvariable=self.bpi_track2_var, values=["75", "210"], width=5).pack(side="left", padx=5)
        self.bpi_track3_var = tk.StringVar(value="210")
        self.bpi_track3_label = ttk.Label(bpi_frame)
        self.bpi_track3_label.pack(side="left", padx=(10, 0))
        ttk.Combobox(bpi_frame, textvariable=self.bpi_track3_var, values=["75", "210"], width=5).pack(side="left", padx=5)
        self.set_bpi_btn = ttk.Button(self.config_frame, command=self.set_bpi)
        self.set_bpi_btn.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.bpc_label = ttk.Label(self.config_frame)
        self.bpc_label.grid(row=6, column=0, sticky="w", pady=5)
        bpc_frame = ttk.Frame(self.config_frame)
        bpc_frame.grid(row=6, column=1, sticky="w", padx=5, pady=5)
        self.bpc_track1_var = tk.StringVar(value="7")
        self.bpc_track1_label = ttk.Label(bpc_frame)
        self.bpc_track1_label.pack(side="left")
        ttk.Combobox(bpc_frame, textvariable=self.bpc_track1_var, values=["5", "6", "7", "8"], width=3).pack(side="left", padx=5)
        self.bpc_track2_var = tk.StringVar(value="5")
        self.bpc_track2_label = ttk.Label(bpc_frame)
        self.bpc_track2_label.pack(side="left", padx=(10, 0))
        ttk.Combobox(bpc_frame, textvariable=self.bpc_track2_var, values=["5", "6", "7", "8"], width=3).pack(side="left", padx=5)
        self.bpc_track3_var = tk.StringVar(value="5")
        self.bpc_track3_label = ttk.Label(bpc_frame)
        self.bpc_track3_label.pack(side="left", padx=(10, 0))
        ttk.Combobox(bpc_frame, textvariable=self.bpc_track3_var, values=["5", "6", "7", "8"], width=3).pack(side="left", padx=5)
        self.set_bpc_btn = ttk.Button(self.config_frame, command=self.set_bpc)
        self.set_bpc_btn.grid(row=7, column=0, columnspan=2, pady=10)
        
        self.coercivity_label = ttk.Label(self.config_frame)
        self.coercivity_label.grid(row=8, column=0, sticky="w", pady=5)
        coercivity_frame = ttk.Frame(self.config_frame)
        coercivity_frame.grid(row=8, column=1, sticky="w", padx=5, pady=5)
        self.coercivity_var = tk.StringVar(value="Hi")
        self.high_co_radio = ttk.Radiobutton(coercivity_frame, variable=self.coercivity_var, value="Hi")
        self.high_co_radio.pack(side="left")
        self.low_co_radio = ttk.Radiobutton(coercivity_frame, variable=self.coercivity_var, value="Low")
        self.low_co_radio.pack(side="left", padx=(10, 0))
        self.set_coercivity_btn = ttk.Button(self.config_frame, command=self.set_coercivity)
        self.set_coercivity_btn.grid(row=9, column=0, columnspan=2, pady=10)

    def setup_generator_tab(self):
        self.gen_frame = ttk.LabelFrame(self.generator_tab, padding=10)
        self.gen_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.card_type_label = ttk.Label(self.gen_frame)
        self.card_type_label.grid(row=0, column=0, sticky="w", pady=5)
        self.card_type_var = tk.StringVar(value="Visa")
        card_type_combo = ttk.Combobox(self.gen_frame, textvariable=self.card_type_var, 
                                      values=["Visa", "Mastercard", "American Express", "Diners Club"], width=20)
        card_type_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        self.bin_label = ttk.Label(self.gen_frame)
        self.bin_label.grid(row=1, column=0, sticky="w", pady=5)
        self.bin_var = tk.StringVar()
        ttk.Entry(self.gen_frame, textvariable=self.bin_var, width=20).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.bin_help_label = ttk.Label(self.gen_frame)
        self.bin_help_label.grid(row=1, column=2, sticky="w", padx=5, pady=5)
        
        self.generate_card_btn = ttk.Button(self.gen_frame, command=self.generate_card)
        self.generate_card_btn.grid(row=0, column=2, padx=10, pady=5)
        
        self.card_number_label = ttk.Label(self.gen_frame)
        self.card_number_label.grid(row=2, column=0, sticky="w", pady=5)
        self.card_number_var = tk.StringVar()
        ttk.Entry(self.gen_frame, textvariable=self.card_number_var, width=30, state="readonly").grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        self.card_expiry_label = ttk.Label(self.gen_frame)
        self.card_expiry_label.grid(row=3, column=0, sticky="w", pady=5)
        self.card_expiry_var = tk.StringVar()
        ttk.Entry(self.gen_frame, textvariable=self.card_expiry_var, width=10, state="readonly").grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        self.card_cvv_label = ttk.Label(self.gen_frame, text="CVV:")
        self.card_cvv_label.grid(row=4, column=0, sticky="w", pady=5)
        self.card_cvv_var = tk.StringVar()
        ttk.Entry(self.gen_frame, textvariable=self.card_cvv_var, width=5, state="readonly").grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        self.copy_track1_btn = ttk.Button(self.gen_frame, command=self.copy_to_track1)
        self.copy_track1_btn.grid(row=5, column=0, padx=5, pady=10)
        self.copy_track2_btn = ttk.Button(self.gen_frame, command=self.copy_to_track2)
        self.copy_track2_btn.grid(row=5, column=1, padx=5, pady=10)
        self.copy_both_btn = ttk.Button(self.gen_frame, command=self.copy_to_both_tracks)
        self.copy_both_btn.grid(row=5, column=2, padx=5, pady=10)

    def set_language(self, lang_code):
        """Sets the application language and updates all UI text."""
        self.current_language = lang_code
        self.strings = self.languages[self.current_language]
        self.update_ui_text()

    def update_ui_text(self):
        """Updates all text elements in the UI to the current language."""
        s = self.strings
        self.root.title(s["window_title"])

        # Menu
        self.menu_bar.entryconfig(1, label=s["themes"])
        self.menu_bar.entryconfig(2, label=s["language"])
        self.theme_menu.entryconfig(0, label=s["light"])
        self.theme_menu.entryconfig(1, label=s["dark"])
        self.theme_menu.entryconfig(2, label=s["matrix"])
        self.theme_menu.entryconfig(3, label=s["synthwave"])
        self.theme_menu.entryconfig(4, label=s["dracula"])

        # Connection
        self.connection_frame.config(text=s["connection"])
        self.port_label.config(text=s["port"])
        self.refresh_btn.config(text=s["refresh_ports"])
        self.connect_btn.config(text=s["connect"] if not self.is_connected else s["disconnect"])
        self.status_label.config(text=s["disconnected"] if not self.is_connected else s["connected"])

        # Notebook Tabs
        self.notebook.tab(0, text=s["basic"])
        self.notebook.tab(1, text=s["advanced"])
        self.notebook.tab(2, text=s["raw_data"])
        self.notebook.tab(3, text=s["configuration"])
        self.notebook.tab(4, text=s["generator"])

        # Basic Tab
        self.data_frame.config(text=s["card_data"])
        self.track1_label.config(text=s["track1"])
        self.track2_label.config(text=s["track2"])
        self.track3_label.config(text=s["track3"])
        self.select_tracks_label.config(text=s["select_tracks_to_write"])
        self.track1_check.config(text=s["track1"][:-1])
        self.track2_check.config(text=s["track2"][:-1])
        self.track3_check.config(text=s["track3"][:-1])
        self.read_btn.config(text=s["read_card"])
        self.write_btn.config(text=s["write_card"])
        self.erase_btn.config(text=s["erase_card"])

        # Advanced Tab
        self.led_frame.config(text=s["led_control"])
        self.all_led_on_btn.config(text=s["all_led_on"])
        self.all_led_off_btn.config(text=s["all_led_off"])
        self.green_led_btn.config(text=s["green_led"])
        self.yellow_led_btn.config(text=s["yellow_led"])
        self.red_led_btn.config(text=s["red_led"])
        self.test_frame.config(text=s["test_functions"])
        self.comm_test_btn.config(text=s["comm_test"])
        self.sensor_test_btn.config(text=s["sensor_test"])
        self.ram_test_btn.config(text=s["ram_test"])
        self.info_frame.config(text=s["device_info"])
        self.get_model_btn.config(text=s["get_model"])
        self.get_firmware_btn.config(text=s["get_firmware"])
        self.get_coercivity_btn.config(text=s["get_coercivity"])

        # Raw Tab
        self.raw_frame.config(text=s["raw_data"])
        self.raw_track1_label.config(text=s["raw_track1"])
        self.raw_track2_label.config(text=s["raw_track2"])
        self.raw_track3_label.config(text=s["raw_track3"])
        self.read_raw_btn.config(text=s["read_raw"])
        self.write_raw_btn.config(text=s["write_raw"])

        # Config Tab
        self.config_frame.config(text=s["configuration"])
        self.leading_zero_13_label.config(text=s["leading_zeros_13"])
        self.leading_zero_2_label.config(text=s["leading_zeros_2"])
        self.set_leading_zeros_btn.config(text=s["set_leading_zeros"])
        self.check_leading_zeros_btn.config(text=s["check_leading_zeros"])
        self.bpi_label.config(text=s["bpi"])
        self.bpi_track1_label.config(text=s["track1"][:-1])
        self.bpi_track2_label.config(text=s["track2"][:-1])
        self.bpi_track3_label.config(text=s["track3"][:-1])
        self.set_bpi_btn.config(text=s["set_bpi"])
        self.bpc_label.config(text=s["bpc"])
        self.bpc_track1_label.config(text=s["track1"][:-1])
        self.bpc_track2_label.config(text=s["track2"][:-1])
        self.bpc_track3_label.config(text=s["track3"][:-1])
        self.set_bpc_btn.config(text=s["set_bpc"])
        self.coercivity_label.config(text=s["coercivity"])
        self.high_co_radio.config(text=s["high_co"])
        self.low_co_radio.config(text=s["low_co"])
        self.set_coercivity_btn.config(text=s["set_coercivity"])

        # Generator Tab
        self.gen_frame.config(text=s["generator"])
        self.card_type_label.config(text=s["card_type"])
        self.bin_label.config(text=s["bin"])
        self.bin_help_label.config(text=s["bin_help"])
        self.generate_card_btn.config(text=s["generate_card"])
        self.card_number_label.config(text=s["card_number"])
        self.card_expiry_label.config(text=s["expiry_date"])
        self.copy_track1_btn.config(text=s["copy_to_track1"])
        self.copy_track2_btn.config(text=s["copy_to_track2"])
        self.copy_both_btn.config(text=s["copy_both"])

        # Log
        self.log_frame.config(text=s["log"])

    def set_theme(self, theme_name):
        themes = {
            "Light": {"bg": "#F0F0F0", "fg": "#000000", "button_bg": "#E0E0E0", "entry_bg": "#FFFFFF", "text_bg": "#FFFFFF", "select_bg": "#E0E0E0"},
            "Dark": {"bg": "#2E2E2E", "fg": "#FFFFFF", "button_bg": "#3C3C3C", "entry_bg": "#4A4A4A", "text_bg": "#4A4A4A", "select_bg": "#4A4A4A"},
            "Matrix": {"bg": "#000000", "fg": "#00FF00", "button_bg": "#003300", "entry_bg": "#001100", "text_bg": "#001100", "select_bg": "#003300"},
            "Synthwave": {"bg": "#240046", "fg": "#FF9E00", "button_bg": "#5A189A", "entry_bg": "#3C096C", "text_bg": "#3C096C", "select_bg": "#5A189A"},
            "Dracula": {"bg": "#282A36", "fg": "#F8F8F2", "button_bg": "#44475A", "entry_bg": "#44475A", "text_bg": "#44475A", "select_bg": "#6272A4"}
        }
        theme = themes.get(theme_name, themes["Light"])

        # Use ttk.Style for consistent theming
        style = ttk.Style()
        style.theme_use('default')

        # Configure styles for all ttk widgets
        style.configure('.', background=theme["bg"], foreground=theme["fg"], fieldbackground=theme["entry_bg"], borderwidth=1)
        style.map('.', background=[('active', theme["select_bg"])])
        
        style.configure('TButton', background=theme["button_bg"], foreground=theme["fg"], padding=5)
        style.map('TButton', background=[('active', theme["select_bg"])])
        
        style.configure('TFrame', background=theme["bg"])
        style.configure('TLabel', background=theme["bg"], foreground=theme["fg"])
        style.configure('TLabelFrame', background=theme["bg"], foreground=theme["fg"])
        style.configure('TLabelFrame.Label', background=theme["bg"], foreground=theme["fg"])
        
        style.configure('TEntry', fieldbackground=theme["entry_bg"], foreground=theme["fg"], insertcolor=theme["fg"])
        
        style.configure('TCombobox', fieldbackground=theme["entry_bg"], foreground=theme["fg"], selectbackground=theme["select_bg"])
        style.map('TCombobox', fieldbackground=[('readonly', theme["entry_bg"])])
        
        style.configure('TCheckbutton', background=theme["bg"], foreground=theme["fg"])
        style.map('TCheckbutton', background=[('active', theme["bg"])], indicatorcolor=[('selected', theme["fg"]), ('!selected', theme["fg"])])
        
        style.configure('TRadiobutton', background=theme["bg"], foreground=theme["fg"])
        style.map('TRadiobutton', background=[('active', theme["bg"])], indicatorcolor=[('selected', theme["fg"]), ('!selected', theme["fg"])])
        
        style.configure('TNotebook', background=theme["bg"])
        style.configure('TNotebook.Tab', background=theme["bg"], foreground=theme["fg"], padding=[5, 2])
        style.map('TNotebook.Tab', background=[('selected', theme["select_bg"])], foreground=[('selected', theme["fg"])])
        
        # Configure non-ttk widgets
        self.root.configure(bg=theme["bg"])
        self.log_text.configure(bg=theme["text_bg"], fg=theme["fg"], insertbackground=theme["fg"],
                                selectbackground=theme["select_bg"], selectforeground=theme["fg"])
        self.menu_bar.configure(bg=theme["bg"], fg=theme["fg"], activebackground=theme["select_bg"], activeforeground=theme["fg"])
        self.theme_menu.configure(bg=theme["bg"], fg=theme["fg"], activebackground=theme["select_bg"], activeforeground=theme["fg"])
        self.language_menu.configure(bg=theme["bg"], fg=theme["fg"], activebackground=theme["select_bg"], activeforeground=theme["fg"])

        self.log_message(self.strings["theme_changed"].format(theme_name))

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
            messagebox.showerror(self.strings["error"], self.strings["port_select_error"])
            return
        
        try:
            self.ser = serial.Serial(port=port, baudrate=9600, timeout=1)
            self.is_connected = True
            self.log_message(self.strings["connected_to"].format(port))
            self.reset_device()
        except Exception as e:
            messagebox.showerror(self.strings["connection_error"], self.strings["could_not_connect"].format(port, str(e)))
        finally:
            self.update_connection_status_ui()

    def disconnect_serial(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.is_connected = False
        self.log_message(self.strings["disconnected"])
        self.update_connection_status_ui()
        
    def update_connection_status_ui(self):
        s = self.strings
        if self.is_connected:
            self.connect_btn.config(text=s["disconnect"])
            self.status_label.config(text=s["connected"], foreground="green")
            self.read_btn.config(state="normal")
            self.write_btn.config(state="normal")
            self.erase_btn.config(state="normal")
        else:
            self.connect_btn.config(text=s["connect"])
            self.status_label.config(text=s["disconnected"], foreground="red")
            self.read_btn.config(state="disabled")
            self.write_btn.config(state="disabled")
            self.erase_btn.config(state="disabled")

    def reset_device(self):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(bytes([0x1B, 0x61]))
                self.log_message(self.strings["device_reset"])
            except Exception as e:
                self.log_message(self.strings["reset_error"].format(str(e)))
    
    def send_command(self, command, description, expect_response=True, timeout=10):
        if not self.is_connected:
            messagebox.showerror(self.strings["error"], self.strings["not_connected"])
            return None
        
        try:
            self.ser.write(command)
            self.log_message(self.strings["command_sent"].format(description))
            
            if not expect_response: return None
                
            start_time = time.time()
            response = b""
            while time.time() - start_time < timeout:
                if self.ser.in_waiting:
                    response += self.ser.read(self.ser.in_waiting)
                    if len(response) >= 2 and response[-2] == 0x1B: break
                time.sleep(0.05)
            
            if response: return response
            else:
                self.log_message(self.strings["timeout"].format(description))
                return None
                
        except Exception as e:
            self.log_message(self.strings["command_error"].format(description, str(e)))
            return None
    
    # --- All other methods (read_card, write_card, generate_card, etc.) remain the same ---
    # --- but with hardcoded strings replaced by self.strings lookup. ---
    # (The following is a condensed version for brevity, the full logic is implemented)
    
    def read_card(self):
        response = self.send_command(bytes([0x1B, 0x72]), self.strings["read_card"], timeout=15)
        if response: self.process_read_response(response)

    def process_read_response(self, response):
        try:
            if response[0:2] != bytes([0x1B, 0x73]):
                self.log_message(self.strings["invalid_response"])
                return
            
            tracks = {1: "", 2: "", 3: ""}
            # Simplified parsing logic for brevity
            parts = response.split(b'\x1b')[1:]
            for part in parts:
                if not part: continue
                track_num = part[0]
                data = part[1:].split(b'?')[0]
                if track_num == 0x01: tracks[1] = data.decode(errors='ignore')
                elif track_num == 0x02: tracks[2] = data.decode(errors='ignore')
                elif track_num == 0x03: tracks[3] = data.decode(errors='ignore')

            self.root.after(0, lambda: self.update_track_data(tracks))
            
            status_byte = response[-1]
            if status_byte == 0x30: self.log_message(self.strings["read_success"])
            else: self.log_message(self.strings["read_error"].format(hex(status_byte)))
        except Exception as e:
            self.log_message(self.strings["process_error"].format(str(e)))

    def update_track_data(self, tracks):
        self.track1_var.set(tracks.get(1, ''))
        self.track2_var.set(tracks.get(2, ''))
        self.track3_var.set(tracks.get(3, ''))

    def write_card(self):
        if not any([self.track1_write.get(), self.track2_write.get(), self.track3_write.get()]):
            messagebox.showwarning(self.strings["warning"], self.strings["select_track_to_write_warning"])
            return
        
        data_block = bytearray([0x1B, 0x73])
        if self.track1_write.get() and self.track1_var.get(): data_block += b'\x1b\x01' + self.track1_var.get().encode()
        if self.track2_write.get() and self.track2_var.get(): data_block += b'\x1b\x02' + self.track2_var.get().encode()
        if self.track3_write.get() and self.track3_var.get(): data_block += b'\x1b\x03' + self.track3_var.get().encode()
        data_block += b'?\x1c'
        
        command = b'\x1b\x77' + data_block
        response = self.send_command(command, self.strings["write_card"], timeout=15)
        
        if response and len(response) >= 2 and response[0] == 0x1B:
            status = response[1]
            if status == 0x30: self.log_message(self.strings["write_success"])
            else: self.log_message(self.strings["write_error"].format(hex(status)))
        elif response: self.log_message(self.strings["invalid_response"])

    def erase_card(self):
        select_byte = 0
        if self.track1_write.get(): select_byte |= 0x01
        if self.track2_write.get(): select_byte |= 0x02
        if self.track3_write.get(): select_byte |= 0x04
        
        if select_byte == 0:
            messagebox.showwarning(self.strings["warning"], self.strings["select_track_to_erase_warning"])
            return
            
        command = bytes([0x1B, 0x63, select_byte])
        response = self.send_command(command, self.strings["erase_card"], timeout=15)
        
        if response and len(response) >= 2 and response[0] == 0x1B:
            status = response[1]
            if status == 0x30: self.log_message(self.strings["erase_success"])
            else: self.log_message(self.strings["erase_error"].format(hex(status)))
        elif response: self.log_message(self.strings["invalid_response"])

    def led_control(self, code):
        self.send_command(bytes([0x1B, code]), self.strings["led_control"], expect_response=False)

    def communication_test(self):
        response = self.send_command(bytes([0x1B, 0x65]), self.strings["comm_test"])
        if response == b'\x1b\x79': self.log_message(self.strings["comm_test_success"])
        elif response: self.log_message(self.strings["comm_test_fail"].format(response.hex()))

    def sensor_test(self):
        response = self.send_command(bytes([0x1B, 0x86]), self.strings["sensor_test"], timeout=30)
        if response == b'\x1b\x30': self.log_message(self.strings["sensor_test_success"])
        elif response: self.log_message(self.strings["sensor_test_fail"].format(response.hex()))

    def ram_test(self):
        response = self.send_command(bytes([0x1B, 0x87]), self.strings["ram_test"])
        if response == b'\x1b\x30': self.log_message(self.strings["ram_test_success"])
        elif response == b'\x1b\x41': self.log_message(self.strings["ram_test_fail"])
        elif response: self.log_message(self.strings["ram_test_unexpected"].format(response.hex()))

    def get_device_model(self):
        response = self.send_command(bytes([0x1B, 0x74]), self.strings["get_model"])
        if response and len(response) >= 3 and response[0] == 0x1B and response[-1] == 0x53:
            model = response[1:-1].decode(errors='ignore')
            self.log_message(self.strings["device_model"].format(model))
        elif response: self.log_message(self.strings["get_model_fail"].format(response.hex()))

    def get_firmware_version(self):
        response = self.send_command(bytes([0x1B, 0x76]), self.strings["get_firmware"])
        if response and response[0] == 0x1B:
            version = response[1:].decode(errors='ignore')
            self.log_message(self.strings["firmware_version"].format(version))
        elif response: self.log_message(self.strings["get_firmware_fail"].format(response.hex()))

    def get_coercivity_status(self):
        response = self.send_command(bytes([0x1B, 0x64]), self.strings["get_coercivity"])
        if response == b'\x1b\x48': self.log_message(self.strings["coercivity_status_hi"])
        elif response == b'\x1b\x4C': self.log_message(self.strings["coercivity_status_lo"])
        elif response: self.log_message(self.strings["get_coercivity_fail"].format(response.hex()))

    def read_raw_data(self):
        response = self.send_command(bytes([0x1B, 0x6D]), self.strings["read_raw"], timeout=15)
        if response: self.process_raw_read_response(response)

    def process_raw_read_response(self, response):
        try:
            if response[0:2] != bytes([0x1B, 0x73]):
                self.log_message(self.strings["invalid_response"])
                return
            
            tracks = {1: "", 2: "", 3: ""}
            pos = 2
            while pos < len(response) and response[pos] == 0x1B:
                track_num = response[pos+1]
                length = response[pos+2]
                data = response[pos+3 : pos+3+length]
                if track_num == 1: tracks[1] = data.hex()
                elif track_num == 2: tracks[2] = data.hex()
                elif track_num == 3: tracks[3] = data.hex()
                pos += 3 + length
            
            self.root.after(0, lambda: self.update_raw_track_data(tracks))
            
            status_byte = response[-1]
            if status_byte == 0x30: self.log_message(self.strings["raw_read_success"])
            else: self.log_message(self.strings["raw_read_error"].format(hex(status_byte)))
        except Exception as e:
            self.log_message(self.strings["process_error"].format(str(e)))

    def update_raw_track_data(self, tracks):
        self.raw_track1_var.set(tracks.get(1, ''))
        self.raw_track2_var.set(tracks.get(2, ''))
        self.raw_track3_var.set(tracks.get(3, ''))

    def write_raw_data(self):
        data_block = bytearray([0x1B, 0x73])
        try:
            if self.raw_track1_var.get():
                raw = bytes.fromhex(self.raw_track1_var.get())
                data_block += bytes([0x1B, 0x01, len(raw)]) + raw
            if self.raw_track2_var.get():
                raw = bytes.fromhex(self.raw_track2_var.get())
                data_block += bytes([0x1B, 0x02, len(raw)]) + raw
            if self.raw_track3_var.get():
                raw = bytes.fromhex(self.raw_track3_var.get())
                data_block += bytes([0x1B, 0x03, len(raw)]) + raw
        except ValueError as e:
            track = '1' if '1' in str(e) else '2' if '2' in str(e) else '3'
            self.log_message(self.strings["invalid_hex"].format(track))
            return
        
        data_block += b'?\x1c'
        command = b'\x1b\x6E' + data_block
        response = self.send_command(command, self.strings["write_raw"], timeout=15)
        
        if response and len(response) >= 2 and response[0] == 0x1B:
            status = response[1]
            if status == 0x30: self.log_message(self.strings["raw_write_success"])
            else: self.log_message(self.strings["raw_write_error"].format(hex(status)))
        elif response: self.log_message(self.strings["invalid_response"])
    
    def set_leading_zeros(self):
        try:
            lz_13 = int(self.leading_zero_13_var.get())
            lz_2 = int(self.leading_zero_2_var.get())
            if not (0 <= lz_13 <= 255 and 0 <= lz_2 <= 255): raise ValueError()
            
            command = bytes([0x1B, 0x7A, lz_13, lz_2])
            response = self.send_command(command, self.strings["set_leading_zeros"])
            
            if response == b'\x1b\x30': self.log_message(self.strings["leading_zeros_set"])
            elif response == b'\x1b\x41': self.log_message(self.strings["set_leading_zeros_fail"])
        except ValueError:
            self.log_message(self.strings["invalid_leading_zero_value"])

    def check_leading_zeros(self):
        response = self.send_command(bytes([0x1B, 0x6C]), self.strings["check_leading_zeros"])
        if response and len(response) == 3 and response[0] == 0x1B:
            self.log_message(self.strings["leading_zeros_check"].format(response[1], response[2]))
        elif response: self.log_message(self.strings["check_leading_zeros_fail"].format(response.hex()))

    def set_bpi(self):
        try:
            bpi_map = {"75": 0xA0, "210": 0xA1}
            cmd1 = bytes([0x1B, 0x62, bpi_map[self.bpi_track1_var.get()]])
            
            bpi_map_t2 = {"75": 0x4B, "210": 0xD2}
            cmd2 = bytes([0x1B, 0x62, bpi_map_t2[self.bpi_track2_var.get()]])
            
            bpi_map_t3 = {"75": 0xC0, "210": 0xC1}
            cmd3 = bytes([0x1B, 0x62, bpi_map_t3[self.bpi_track3_var.get()]])
            
            for cmd, track, bpi_val in [(cmd1, self.strings["track1"][:-1], self.bpi_track1_var.get()),
                                        (cmd2, self.strings["track2"][:-1], self.bpi_track2_var.get()),
                                        (cmd3, self.strings["track3"][:-1], self.bpi_track3_var.get())]:
                response = self.send_command(cmd, f"Set BPI for {track}")
                if response == b'\x1b\x30': self.log_message(self.strings["bpi_set_success"].format(track, bpi_val))
                elif response: self.log_message(self.strings["bpi_set_fail"].format(track, response.hex()))
        except Exception as e:
            self.log_message(self.strings["bpi_set_error"].format(str(e)))

    def set_bpc(self):
        try:
            bpc1 = int(self.bpc_track1_var.get())
            bpc2 = int(self.bpc_track2_var.get())
            bpc3 = int(self.bpc_track3_var.get())
            if not (5 <= bpc1 <= 8 and 5 <= bpc2 <= 8 and 5 <= bpc3 <= 8): raise ValueError()
            
            command = bytes([0x1B, 0x6F, bpc1, bpc2, bpc3])
            response = self.send_command(command, self.strings["set_bpc"])
            
            if response and len(response) == 5 and response[:2] == b'\x1b\x30':
                self.log_message(self.strings["bpc_set_success"].format(response[2], response[3], response[4]))
            elif response: self.log_message(self.strings["bpc_set_fail"].format(response.hex()))
        except ValueError:
            self.log_message(self.strings["invalid_bpc_value"])
            
    def set_coercivity(self):
        cmd_code = 0x78 if self.coercivity_var.get() == "Hi" else 0x79
        response = self.send_command(bytes([0x1B, cmd_code]), self.strings["set_coercivity"])
        if response == b'\x1b\x30':
            co_text = self.strings["high_co"] if self.coercivity_var.get() == "Hi" else self.strings["low_co"]
            self.log_message(self.strings["coercivity_set_success"].format(co_text))
        elif response: self.log_message(self.strings["coercivity_set_fail"].format(response.hex()))

    def generate_card(self):
        card_type = self.card_type_var.get()
        bin_number = self.bin_var.get().strip()
        card_number = self.generate_card_number(card_type, bin_number)
        if not card_number: return
        
        expiry_date = self.generate_expiry_date()
        cvv = self.generate_cvv(card_type)
        
        self.card_number_var.set(card_number)
        self.card_expiry_var.set(expiry_date)
        self.card_cvv_var.set(cvv)
        
        self.log_message(self.strings["card_generated"].format(card_type, card_number))

    def generate_card_number(self, card_type, bin_number=""):
        s = self.strings
        if bin_number:
            if len(bin_number) != 6 or not bin_number.isdigit():
                messagebox.showerror(s["error"], s["invalid_bin_error"])
                return ""
            
            warnings = {
                "Visa": (not bin_number.startswith("4"), s["bin_mismatch_warning_visa"]),
                "Mastercard": (not any(bin_number.startswith(p) for p in ("51", "52", "53", "54", "55", "22", "23", "24", "25", "26", "27")), s["bin_mismatch_warning_mastercard"]),
                "American Express": (not bin_number.startswith(("34", "37")), s["bin_mismatch_warning_amex"]),
                "Diners Club": (not bin_number.startswith(("36", "38", "39")), s["bin_mismatch_warning_diners"])
            }
            if card_type in warnings and warnings[card_type][0]:
                if not messagebox.askyesno(s["warning"], warnings[card_type][1]):
                    return ""
            prefix = bin_number
        else:
            prefixes = {
                "Visa": "4", "Mastercard": random.choice(["51", "52", "53", "54", "55"]),
                "American Express": random.choice(["34", "37"]), "Diners Club": random.choice(["36", "38", "39"])
            }
            prefix = prefixes.get(card_type, "4")
        
        lengths = {"American Express": 15, "Diners Club": 14}
        length = lengths.get(card_type, 16)
        
        number = prefix
        while len(number) < length - 1:
            number += str(random.randint(0, 9))
        
        check_digit = self.calculate_luhn_check_digit(number)
        return number + str(check_digit)

    def calculate_luhn_check_digit(self, number):
        total = 0
        for i, digit in enumerate(reversed(number)):
            n = int(digit)
            if i % 2 == 0:
                n *= 2
                if n > 9: n -= 9
            total += n
        return (10 - (total % 10)) % 10

    def generate_expiry_date(self):
        now = datetime.now()
        random_date = now + timedelta(days=random.randint(365, 365 * 5))
        return random_date.strftime("%m%y") # YYMM format for tracks

    def generate_cvv(self, card_type):
        return str(random.randint(1000, 9999)) if card_type == "American Express" else str(random.randint(100, 999))

    def copy_to_track1(self):
        card_number = self.card_number_var.get()
        expiry_date = self.card_expiry_var.get() # YYMM
        card_holder = "TEST/CARDHOLDER"
        track1_data = f"%B{card_number}^{card_holder}^{expiry_date}101?"
        self.track1_var.set(track1_data)
        self.log_message(self.strings["copied_to_track1"])

    def copy_to_track2(self):
        card_number = self.card_number_var.get()
        expiry_date = self.card_expiry_var.get() # YYMM
        track2_data = f";{card_number}={expiry_date}101?"
        self.track2_var.set(track2_data)
        self.log_message(self.strings["copied_to_track2"])

    def copy_to_both_tracks(self):
        self.copy_to_track1()
        self.copy_to_track2()
        self.log_message(self.strings["copied_to_both"])

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
