import sys
import time
import random
from datetime import datetime, timedelta
import serial
import serial.tools.list_ports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QComboBox, QTabWidget, QTextEdit,
    QCheckBox, QRadioButton, QMessageBox, QMenuBar
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QPalette, QColor, QTextCursor

class MSRE206_Qt_App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ser = None
        self.is_connected = False

        # --- Internationalization (i18n) Setup ---
        # Samma språkdata som i originalet
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
        self.current_language = "SV"  # Starta med svenska
        self.strings = self.languages[self.current_language]

        self.init_ui()
        self.create_themes()
        self.set_theme("Light") # Standardtema
        self.auto_detect_port()
        self.update_ui_text()

    def init_ui(self):
        """Skapar och organiserar alla UI-komponenter."""
        self.setWindowTitle(self.strings["window_title"])
        self.setGeometry(100, 100, 900, 800)

        # Huvud-widget och layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        self.create_menu()

        # Skapa UI-sektioner
        main_layout.addWidget(self.create_connection_group())
        
        self.notebook = QTabWidget()
        self.setup_tabs()
        main_layout.addWidget(self.notebook)

        main_layout.addWidget(self.create_log_group())

        self.update_connection_status_ui()

    def create_menu(self):
        """Skapar menyraden för teman och språk."""
        self.menu_bar = self.menuBar()

        # Temameny
        self.theme_menu = self.menu_bar.addMenu("")
        self.theme_light_action = QAction("", self)
        self.theme_light_action.triggered.connect(lambda: self.set_theme("Light"))
        self.theme_menu.addAction(self.theme_light_action)
        
        self.theme_dark_action = QAction("", self)
        self.theme_dark_action.triggered.connect(lambda: self.set_theme("Dark"))
        self.theme_menu.addAction(self.theme_dark_action)

        self.theme_matrix_action = QAction("", self)
        self.theme_matrix_action.triggered.connect(lambda: self.set_theme("Matrix"))
        self.theme_menu.addAction(self.theme_matrix_action)

        self.theme_synthwave_action = QAction("", self)
        self.theme_synthwave_action.triggered.connect(lambda: self.set_theme("Synthwave"))
        self.theme_menu.addAction(self.theme_synthwave_action)

        self.theme_dracula_action = QAction("", self)
        self.theme_dracula_action.triggered.connect(lambda: self.set_theme("Dracula"))
        self.theme_menu.addAction(self.theme_dracula_action)

        # Språkmeny
        self.language_menu = self.menu_bar.addMenu("")
        en_action = QAction("English", self)
        en_action.triggered.connect(lambda: self.set_language("EN"))
        self.language_menu.addAction(en_action)
        
        sv_action = QAction("Svenska", self)
        sv_action.triggered.connect(lambda: self.set_language("SV"))
        self.language_menu.addAction(sv_action)

    def create_connection_group(self):
        """Skapar gruppen för anslutningsinställningar."""
        self.connection_group = QGroupBox()
        layout = QHBoxLayout(self.connection_group)

        self.port_label = QLabel()
        layout.addWidget(self.port_label)

        self.port_combo = QComboBox()
        layout.addWidget(self.port_combo)

        self.refresh_btn = QPushButton()
        self.refresh_btn.clicked.connect(self.refresh_ports)
        layout.addWidget(self.refresh_btn)

        self.connect_btn = QPushButton()
        self.connect_btn.clicked.connect(self.toggle_connection)
        layout.addWidget(self.connect_btn)

        self.status_label = QLabel()
        layout.addWidget(self.status_label)
        layout.addStretch(1) # Fyller ut resten av utrymmet

        return self.connection_group

    def setup_tabs(self):
        """Skapar alla flikar i applikationen."""
        self.basic_tab = QWidget()
        self.setup_basic_tab()
        self.notebook.addTab(self.basic_tab, "")

        self.advanced_tab = QWidget()
        self.setup_advanced_tab()
        self.notebook.addTab(self.advanced_tab, "")

        self.raw_tab = QWidget()
        self.setup_raw_tab()
        self.notebook.addTab(self.raw_tab, "")

        self.config_tab = QWidget()
        self.setup_config_tab()
        self.notebook.addTab(self.config_tab, "")

        self.generator_tab = QWidget()
        self.setup_generator_tab()
        self.notebook.addTab(self.generator_tab, "")

    def setup_basic_tab(self):
        """Skapar innehållet för 'Grundläggande'-fliken."""
        layout = QVBoxLayout(self.basic_tab)
        self.data_group = QGroupBox()
        data_layout = QVBoxLayout(self.data_group)
        
        # Track 1, 2, 3
        self.track1_label = QLabel()
        self.track1_edit = QLineEdit()
        data_layout.addWidget(self.track1_label)
        data_layout.addWidget(self.track1_edit)

        self.track2_label = QLabel()
        self.track2_edit = QLineEdit()
        data_layout.addWidget(self.track2_label)
        data_layout.addWidget(self.track2_edit)

        self.track3_label = QLabel()
        self.track3_edit = QLineEdit()
        data_layout.addWidget(self.track3_label)
        data_layout.addWidget(self.track3_edit)

        # Checkboxar för val av spår
        self.select_tracks_label = QLabel()
        data_layout.addWidget(self.select_tracks_label)
        
        checkbox_layout = QHBoxLayout()
        self.track1_check = QCheckBox()
        self.track1_check.setChecked(True)
        self.track2_check = QCheckBox()
        self.track2_check.setChecked(True)
        self.track3_check = QCheckBox()
        self.track3_check.setChecked(True)
        checkbox_layout.addWidget(self.track1_check)
        checkbox_layout.addWidget(self.track2_check)
        checkbox_layout.addWidget(self.track3_check)
        checkbox_layout.addStretch(1)
        data_layout.addLayout(checkbox_layout)

        # Knappar
        button_layout = QHBoxLayout()
        self.read_btn = QPushButton()
        self.read_btn.clicked.connect(self.read_card)
        self.write_btn = QPushButton()
        self.write_btn.clicked.connect(self.write_card)
        self.erase_btn = QPushButton()
        self.erase_btn.clicked.connect(self.erase_card)
        button_layout.addWidget(self.read_btn)
        button_layout.addWidget(self.write_btn)
        button_layout.addWidget(self.erase_btn)
        button_layout.addStretch(1)
        data_layout.addLayout(button_layout)

        data_layout.addStretch(1)
        layout.addWidget(self.data_group)
    
    def setup_advanced_tab(self):
        """Skapar innehållet för 'Avancerat'-fliken."""
        layout = QVBoxLayout(self.advanced_tab)

        # LED-kontroll
        self.led_group = QGroupBox()
        led_layout = QHBoxLayout(self.led_group)
        self.all_led_on_btn = QPushButton()
        self.all_led_on_btn.clicked.connect(lambda: self.led_control(0x82))
        self.all_led_off_btn = QPushButton()
        self.all_led_off_btn.clicked.connect(lambda: self.led_control(0x81))
        self.green_led_btn = QPushButton()
        self.green_led_btn.clicked.connect(lambda: self.led_control(0x83))
        self.yellow_led_btn = QPushButton()
        self.yellow_led_btn.clicked.connect(lambda: self.led_control(0x84))
        self.red_led_btn = QPushButton()
        self.red_led_btn.clicked.connect(lambda: self.led_control(0x85))
        led_layout.addWidget(self.all_led_on_btn)
        led_layout.addWidget(self.all_led_off_btn)
        led_layout.addWidget(self.green_led_btn)
        led_layout.addWidget(self.yellow_led_btn)
        led_layout.addWidget(self.red_led_btn)
        led_layout.addStretch(1)
        layout.addWidget(self.led_group)

        # Testfunktioner
        self.test_group = QGroupBox()
        test_layout = QHBoxLayout(self.test_group)
        self.comm_test_btn = QPushButton()
        self.comm_test_btn.clicked.connect(self.communication_test)
        self.sensor_test_btn = QPushButton()
        self.sensor_test_btn.clicked.connect(self.sensor_test)
        self.ram_test_btn = QPushButton()
        self.ram_test_btn.clicked.connect(self.ram_test)
        test_layout.addWidget(self.comm_test_btn)
        test_layout.addWidget(self.sensor_test_btn)
        test_layout.addWidget(self.ram_test_btn)
        test_layout.addStretch(1)
        layout.addWidget(self.test_group)

        # Enhetsinformation
        self.info_group = QGroupBox()
        info_layout = QHBoxLayout(self.info_group)
        self.get_model_btn = QPushButton()
        self.get_model_btn.clicked.connect(self.get_device_model)
        self.get_firmware_btn = QPushButton()
        self.get_firmware_btn.clicked.connect(self.get_firmware_version)
        self.get_coercivity_btn = QPushButton()
        self.get_coercivity_btn.clicked.connect(self.get_coercivity_status)
        info_layout.addWidget(self.get_model_btn)
        info_layout.addWidget(self.get_firmware_btn)
        info_layout.addWidget(self.get_coercivity_btn)
        info_layout.addStretch(1)
        layout.addWidget(self.info_group)

        layout.addStretch(1)

    def setup_raw_tab(self):
        """Skapar innehållet för 'Rådata'-fliken."""
        layout = QVBoxLayout(self.raw_tab)
        self.raw_group = QGroupBox()
        raw_layout = QVBoxLayout(self.raw_group)

        self.raw_track1_label = QLabel()
        self.raw_track1_edit = QLineEdit()
        raw_layout.addWidget(self.raw_track1_label)
        raw_layout.addWidget(self.raw_track1_edit)

        self.raw_track2_label = QLabel()
        self.raw_track2_edit = QLineEdit()
        raw_layout.addWidget(self.raw_track2_label)
        raw_layout.addWidget(self.raw_track2_edit)

        self.raw_track3_label = QLabel()
        self.raw_track3_edit = QLineEdit()
        raw_layout.addWidget(self.raw_track3_label)
        raw_layout.addWidget(self.raw_track3_edit)

        button_layout = QHBoxLayout()
        self.read_raw_btn = QPushButton()
        self.read_raw_btn.clicked.connect(self.read_raw_data)
        self.write_raw_btn = QPushButton()
        self.write_raw_btn.clicked.connect(self.write_raw_data)
        button_layout.addWidget(self.read_raw_btn)
        button_layout.addWidget(self.write_raw_btn)
        button_layout.addStretch(1)
        raw_layout.addLayout(button_layout)

        raw_layout.addStretch(1)
        layout.addWidget(self.raw_group)

    def setup_config_tab(self):
        """Skapar innehållet för 'Konfiguration'-fliken."""
        layout = QVBoxLayout(self.config_tab)
        self.config_group = QGroupBox()
        config_layout = QVBoxLayout(self.config_group)

        # Ledande nollor
        lz_layout = QHBoxLayout()
        self.leading_zero_13_label = QLabel()
        self.leading_zero_13_edit = QLineEdit("61")
        self.leading_zero_2_label = QLabel()
        self.leading_zero_2_edit = QLineEdit("22")
        lz_layout.addWidget(self.leading_zero_13_label)
        lz_layout.addWidget(self.leading_zero_13_edit)
        lz_layout.addWidget(self.leading_zero_2_label)
        lz_layout.addWidget(self.leading_zero_2_edit)
        lz_layout.addStretch(1)
        config_layout.addLayout(lz_layout)

        lz_btn_layout = QHBoxLayout()
        self.set_leading_zeros_btn = QPushButton()
        self.set_leading_zeros_btn.clicked.connect(self.set_leading_zeros)
        self.check_leading_zeros_btn = QPushButton()
        self.check_leading_zeros_btn.clicked.connect(self.check_leading_zeros)
        lz_btn_layout.addWidget(self.set_leading_zeros_btn)
        lz_btn_layout.addWidget(self.check_leading_zeros_btn)
        lz_btn_layout.addStretch(1)
        config_layout.addLayout(lz_btn_layout)

        # BPI
        self.bpi_label = QLabel()
        config_layout.addWidget(self.bpi_label)
        bpi_layout = QHBoxLayout()
        self.bpi_track1_label = QLabel()
        self.bpi_track1_combo = QComboBox()
        self.bpi_track1_combo.addItems(["75", "210"])
        self.bpi_track1_combo.setCurrentText("210")
        self.bpi_track2_label = QLabel()
        self.bpi_track2_combo = QComboBox()
        self.bpi_track2_combo.addItems(["75", "210"])
        self.bpi_track2_combo.setCurrentText("210")
        self.bpi_track3_label = QLabel()
        self.bpi_track3_combo = QComboBox()
        self.bpi_track3_combo.addItems(["75", "210"])
        self.bpi_track3_combo.setCurrentText("210")
        bpi_layout.addWidget(self.bpi_track1_label)
        bpi_layout.addWidget(self.bpi_track1_combo)
        bpi_layout.addWidget(self.bpi_track2_label)
        bpi_layout.addWidget(self.bpi_track2_combo)
        bpi_layout.addWidget(self.bpi_track3_label)
        bpi_layout.addWidget(self.bpi_track3_combo)
        bpi_layout.addStretch(1)
        config_layout.addLayout(bpi_layout)
        self.set_bpi_btn = QPushButton()
        self.set_bpi_btn.clicked.connect(self.set_bpi)
        config_layout.addWidget(self.set_bpi_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        # BPC
        self.bpc_label = QLabel()
        config_layout.addWidget(self.bpc_label)
        bpc_layout = QHBoxLayout()
        self.bpc_track1_label = QLabel()
        self.bpc_track1_combo = QComboBox()
        self.bpc_track1_combo.addItems(["5", "6", "7", "8"])
        self.bpc_track1_combo.setCurrentText("7")
        self.bpc_track2_label = QLabel()
        self.bpc_track2_combo = QComboBox()
        self.bpc_track2_combo.addItems(["5", "6", "7", "8"])
        self.bpc_track2_combo.setCurrentText("5")
        self.bpc_track3_label = QLabel()
        self.bpc_track3_combo = QComboBox()
        self.bpc_track3_combo.addItems(["5", "6", "7", "8"])
        self.bpc_track3_combo.setCurrentText("5")
        bpc_layout.addWidget(self.bpc_track1_label)
        bpc_layout.addWidget(self.bpc_track1_combo)
        bpc_layout.addWidget(self.bpc_track2_label)
        bpc_layout.addWidget(self.bpc_track2_combo)
        bpc_layout.addWidget(self.bpc_track3_label)
        bpc_layout.addWidget(self.bpc_track3_combo)
        bpc_layout.addStretch(1)
        config_layout.addLayout(bpc_layout)
        self.set_bpc_btn = QPushButton()
        self.set_bpc_btn.clicked.connect(self.set_bpc)
        config_layout.addWidget(self.set_bpc_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        # Koercivitet
        self.coercivity_label = QLabel()
        config_layout.addWidget(self.coercivity_label)
        coercivity_layout = QHBoxLayout()
        self.high_co_radio = QRadioButton()
        self.high_co_radio.setChecked(True)
        self.low_co_radio = QRadioButton()
        coercivity_layout.addWidget(self.high_co_radio)
        coercivity_layout.addWidget(self.low_co_radio)
        coercivity_layout.addStretch(1)
        config_layout.addLayout(coercivity_layout)
        self.set_coercivity_btn = QPushButton()
        self.set_coercivity_btn.clicked.connect(self.set_coercivity)
        config_layout.addWidget(self.set_coercivity_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        config_layout.addStretch(1)
        layout.addWidget(self.config_group)

    def setup_generator_tab(self):
        """Skapar innehållet för 'Kortgenerator'-fliken."""
        layout = QVBoxLayout(self.generator_tab)
        self.gen_group = QGroupBox()
        gen_layout = QVBoxLayout(self.gen_group)

        # Korttyp och BIN
        type_layout = QHBoxLayout()
        self.card_type_label = QLabel()
        self.card_type_combo = QComboBox()
        self.card_type_combo.addItems(["Visa", "Mastercard", "American Express", "Diners Club"])
        self.bin_label = QLabel()
        self.bin_edit = QLineEdit()
        self.bin_help_label = QLabel()
        self.generate_card_btn = QPushButton()
        self.generate_card_btn.clicked.connect(self.generate_card)
        type_layout.addWidget(self.card_type_label)
        type_layout.addWidget(self.card_type_combo)
        type_layout.addWidget(self.bin_label)
        type_layout.addWidget(self.bin_edit)
        type_layout.addWidget(self.bin_help_label)
        type_layout.addWidget(self.generate_card_btn)
        type_layout.addStretch(1)
        gen_layout.addLayout(type_layout)

        # Genererad data
        self.card_number_label = QLabel()
        self.card_number_edit = QLineEdit()
        self.card_number_edit.setReadOnly(True)
        gen_layout.addWidget(self.card_number_label)
        gen_layout.addWidget(self.card_number_edit)

        self.card_expiry_label = QLabel()
        self.card_expiry_edit = QLineEdit()
        self.card_expiry_edit.setReadOnly(True)
        gen_layout.addWidget(self.card_expiry_label)
        gen_layout.addWidget(self.card_expiry_edit)

        self.card_cvv_label = QLabel("CVV:")
        self.card_cvv_edit = QLineEdit()
        self.card_cvv_edit.setReadOnly(True)
        gen_layout.addWidget(self.card_cvv_label)
        gen_layout.addWidget(self.card_cvv_edit)

        # Kopieringsknappar
        copy_layout = QHBoxLayout()
        self.copy_track1_btn = QPushButton()
        self.copy_track1_btn.clicked.connect(self.copy_to_track1)
        self.copy_track2_btn = QPushButton()
        self.copy_track2_btn.clicked.connect(self.copy_to_track2)
        self.copy_both_btn = QPushButton()
        self.copy_both_btn.clicked.connect(self.copy_to_both_tracks)
        copy_layout.addWidget(self.copy_track1_btn)
        copy_layout.addWidget(self.copy_track2_btn)
        copy_layout.addWidget(self.copy_both_btn)
        copy_layout.addStretch(1)
        gen_layout.addLayout(copy_layout)

        gen_layout.addStretch(1)
        layout.addWidget(self.gen_group)

    def create_log_group(self):
        """Skapar loggfönstret."""
        self.log_group = QGroupBox()
        layout = QVBoxLayout(self.log_group)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
        return self.log_group

    def create_themes(self):
        """Definierar QSS (Qt Style Sheets) för de olika teman."""
        self.themes = {
            "Light": """
                QWidget { background-color: #F0F0F0; color: #000000; }
                QMainWindow, QMenuBar, QMenu { background-color: #F0F0F0; color: #000000; }
                QMenuBar::item:selected, QMenu::item:selected { background-color: #B0B0B0; }
                QGroupBox { border: 1px solid #B0B0B0; margin-top: 10px; }
                QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; }
                QPushButton { background-color: #E0E0E0; border: 1px solid #B0B0B0; padding: 5px; border-radius: 3px; }
                QPushButton:hover { background-color: #D0D0D0; }
                QPushButton:pressed { background-color: #C0C0C0; }
                QLineEdit, QComboBox, QTextEdit { background-color: #FFFFFF; border: 1px solid #B0B0B0; border-radius: 3px; }
                QTabWidget::pane { border: 1px solid #B0B0B0; }
                QTabBar::tab { background: #E0E0E0; padding: 8px; border: 1px solid #B0B0B0; }
                QTabBar::tab:selected { background: #F0F0F0; }
            """,
            "Dark": """
                QWidget { background-color: #2E2E2E; color: #FFFFFF; }
                QMainWindow, QMenuBar, QMenu { background-color: #2E2E2E; color: #FFFFFF; }
                QMenuBar::item:selected, QMenu::item:selected { background-color: #4A4A4A; }
                QGroupBox { border: 1px solid #4A4A4A; margin-top: 10px; }
                QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; }
                QPushButton { background-color: #3C3C3C; border: 1px solid #4A4A4A; padding: 5px; border-radius: 3px; }
                QPushButton:hover { background-color: #4A4A4A; }
                QPushButton:pressed { background-color: #5A5A5A; }
                QLineEdit, QComboBox, QTextEdit { background-color: #4A4A4A; border: 1px solid #5A5A5A; border-radius: 3px; color: #FFFFFF; }
                QComboBox::drop-down { border: 0px; }
                QTabWidget::pane { border: 1px solid #4A4A4A; }
                QTabBar::tab { background: #3C3C3C; padding: 8px; border: 1px solid #4A4A4A; }
                QTabBar::tab:selected { background: #2E2E2E; }
            """,
            "Matrix": """
                QWidget { background-color: #000000; color: #00FF00; font-family: 'Courier New', monospace; }
                QMainWindow, QMenuBar, QMenu { background-color: #000000; color: #00FF00; }
                QMenuBar::item:selected, QMenu::item:selected { background-color: #003300; }
                QGroupBox { border: 1px solid #00FF00; margin-top: 10px; }
                QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; }
                QPushButton { background-color: #003300; border: 1px solid #00FF00; padding: 5px; border-radius: 0px; }
                QPushButton:hover { background-color: #005500; }
                QPushButton:pressed { background-color: #007700; }
                QLineEdit, QComboBox, QTextEdit { background-color: #001100; border: 1px solid #00FF00; border-radius: 0px; color: #00FF00; }
                QTabWidget::pane { border: 1px solid #00FF00; }
                QTabBar::tab { background: #003300; padding: 8px; border: 1px solid #00FF00; }
                QTabBar::tab:selected { background: #000000; }
            """,
            "Synthwave": """
                QWidget { background-color: #240046; color: #FF9E00; }
                QMainWindow, QMenuBar, QMenu { background-color: #240046; color: #FF9E00; }
                QMenuBar::item:selected, QMenu::item:selected { background-color: #5A189A; }
                QGroupBox { border: 1px solid #FF9E00; margin-top: 10px; border-radius: 5px; }
                QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; }
                QPushButton { background-color: #5A189A; border: 1px solid #FF9E00; padding: 5px; border-radius: 5px; }
                QPushButton:hover { background-color: #7B2CBF; }
                QPushButton:pressed { background-color: #9D4EDD; }
                QLineEdit, QComboBox, QTextEdit { background-color: #3C096C; border: 1px solid #FF9E00; border-radius: 5px; color: #FF9E00; }
                QTabWidget::pane { border: 1px solid #FF9E00; }
                QTabBar::tab { background: #5A189A; padding: 8px; border: 1px solid #FF9E00; border-top-left-radius: 5px; border-top-right-radius: 5px; }
                QTabBar::tab:selected { background: #240046; }
            """,
            "Dracula": """
                QWidget { background-color: #282a36; color: #f8f8f2; }
                QMainWindow, QMenuBar, QMenu { background-color: #282a36; color: #f8f8f2; }
                QMenuBar::item:selected, QMenu::item:selected { background-color: #44475a; }
                QGroupBox { border: 1px solid #44475a; margin-top: 10px; border-radius: 5px; }
                QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; }
                QPushButton { background-color: #44475a; border: 1px solid #6272a4; padding: 5px; border-radius: 5px; }
                QPushButton:hover { background-color: #6272a4; }
                QPushButton:pressed { background-color: #bd93f9; }
                QLineEdit, QComboBox, QTextEdit { background-color: #44475a; border: 1px solid #6272a4; border-radius: 5px; color: #f8f8f2; }
                QTabWidget::pane { border: 1px solid #44475a; }
                QTabBar::tab { background: #44475a; padding: 8px; border: 1px solid #6272a4; border-top-left-radius: 5px; border-top-right-radius: 5px; }
                QTabBar::tab:selected { background: #282a36; }
            """
        }

    def set_theme(self, theme_name):
        """Applicerar vald QSS-stilmall på applikationen."""
        if theme_name in self.themes:
            self.setStyleSheet(self.themes[theme_name])
            self.log_message(self.strings["theme_changed"].format(theme_name))

    def set_language(self, lang_code):
        """Ställer in programspråket och uppdaterar all UI-text."""
        self.current_language = lang_code
        self.strings = self.languages[self.current_language]
        self.update_ui_text()

    def update_ui_text(self):
        """Uppdaterar alla text-element i UI:t till det valda språket."""
        s = self.strings
        self.setWindowTitle(s["window_title"])

        # Meny
        self.theme_menu.setTitle(s["themes"])
        self.language_menu.setTitle(s["language"])
        self.theme_light_action.setText(s["light"])
        self.theme_dark_action.setText(s["dark"])
        self.theme_matrix_action.setText(s["matrix"])
        self.theme_synthwave_action.setText(s["synthwave"])
        self.theme_dracula_action.setText(s["dracula"])

        # Anslutning
        self.connection_group.setTitle(s["connection"])
        self.port_label.setText(s["port"])
        self.refresh_btn.setText(s["refresh_ports"])
        self.update_connection_status_ui() # Uppdaterar anslut/koppla från knapp och status

        # Flikar
        self.notebook.setTabText(0, s["basic"])
        self.notebook.setTabText(1, s["advanced"])
        self.notebook.setTabText(2, s["raw_data"])
        self.notebook.setTabText(3, s["configuration"])
        self.notebook.setTabText(4, s["generator"])

        # Grundläggande-flik
        self.data_group.setTitle(s["card_data"])
        self.track1_label.setText(s["track1"])
        self.track2_label.setText(s["track2"])
        self.track3_label.setText(s["track3"])
        self.select_tracks_label.setText(s["select_tracks_to_write"])
        self.track1_check.setText(s["track1"][:-1])
        self.track2_check.setText(s["track2"][:-1])
        self.track3_check.setText(s["track3"][:-1])
        self.read_btn.setText(s["read_card"])
        self.write_btn.setText(s["write_card"])
        self.erase_btn.setText(s["erase_card"])

        # Avancerat-flik
        self.led_group.setTitle(s["led_control"])
        self.all_led_on_btn.setText(s["all_led_on"])
        self.all_led_off_btn.setText(s["all_led_off"])
        self.green_led_btn.setText(s["green_led"])
        self.yellow_led_btn.setText(s["yellow_led"])
        self.red_led_btn.setText(s["red_led"])
        self.test_group.setTitle(s["test_functions"])
        self.comm_test_btn.setText(s["comm_test"])
        self.sensor_test_btn.setText(s["sensor_test"])
        self.ram_test_btn.setText(s["ram_test"])
        self.info_group.setTitle(s["device_info"])
        self.get_model_btn.setText(s["get_model"])
        self.get_firmware_btn.setText(s["get_firmware"])
        self.get_coercivity_btn.setText(s["get_coercivity"])

        # Rådata-flik
        self.raw_group.setTitle(s["raw_data"])
        self.raw_track1_label.setText(s["raw_track1"])
        self.raw_track2_label.setText(s["raw_track2"])
        self.raw_track3_label.setText(s["raw_track3"])
        self.read_raw_btn.setText(s["read_raw"])
        self.write_raw_btn.setText(s["write_raw"])

        # Konfiguration-flik
        self.config_group.setTitle(s["configuration"])
        self.leading_zero_13_label.setText(s["leading_zeros_13"])
        self.leading_zero_2_label.setText(s["leading_zeros_2"])
        self.set_leading_zeros_btn.setText(s["set_leading_zeros"])
        self.check_leading_zeros_btn.setText(s["check_leading_zeros"])
        self.bpi_label.setText(s["bpi"])
        self.bpi_track1_label.setText(s["track1"][:-1])
        self.bpi_track2_label.setText(s["track2"][:-1])
        self.bpi_track3_label.setText(s["track3"][:-1])
        self.set_bpi_btn.setText(s["set_bpi"])
        self.bpc_label.setText(s["bpc"])
        self.bpc_track1_label.setText(s["track1"][:-1])
        self.bpc_track2_label.setText(s["track2"][:-1])
        self.bpc_track3_label.setText(s["track3"][:-1])
        self.set_bpc_btn.setText(s["set_bpc"])
        self.coercivity_label.setText(s["coercivity"])
        self.high_co_radio.setText(s["high_co"])
        self.low_co_radio.setText(s["low_co"])
        self.set_coercivity_btn.setText(s["set_coercivity"])

        # Generator-flik
        self.gen_group.setTitle(s["generator"])
        self.card_type_label.setText(s["card_type"])
        self.bin_label.setText(s["bin"])
        self.bin_help_label.setText(s["bin_help"])
        self.generate_card_btn.setText(s["generate_card"])
        self.card_number_label.setText(s["card_number"])
        self.card_expiry_label.setText(s["expiry_date"])
        self.copy_track1_btn.setText(s["copy_to_track1"])
        self.copy_track2_btn.setText(s["copy_to_track2"])
        self.copy_both_btn.setText(s["copy_both"])

        # Logg
        self.log_group.setTitle(s["log"])

    # --- Backend-logik (i stort sett oförändrad från originalet) ---

    def auto_detect_port(self):
        self.refresh_ports()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "USB" in port.description or "Serial" in port.description:
                self.port_combo.setCurrentText(port.device)
                break
    
    def refresh_ports(self):
        self.port_combo.clear()
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo.addItems(ports)
    
    def toggle_connection(self):
        if not self.is_connected:
            self.connect_serial()
        else:
            self.disconnect_serial()
    
    def connect_serial(self):
        port = self.port_combo.currentText()
        if not port:
            QMessageBox.critical(self, self.strings["error"], self.strings["port_select_error"])
            return
        
        try:
            self.ser = serial.Serial(port=port, baudrate=9600, timeout=1)
            self.is_connected = True
            self.log_message(self.strings["connected_to"].format(port))
            self.reset_device()
        except Exception as e:
            QMessageBox.critical(self, self.strings["connection_error"], self.strings["could_not_connect"].format(port, str(e)))
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
        is_enabled = self.is_connected
        
        if is_enabled:
            self.connect_btn.setText(s["disconnect"])
            self.status_label.setText(f"<font color='green'>{s['connected']}</font>")
        else:
            self.connect_btn.setText(s["connect"])
            self.status_label.setText(f"<font color='red'>{s['disconnected']}</font>")
        
        # Aktivera/inaktivera knappar baserat på anslutningsstatus
        self.read_btn.setEnabled(is_enabled)
        self.write_btn.setEnabled(is_enabled)
        self.erase_btn.setEnabled(is_enabled)
        # ... och så vidare för alla andra knappar som kräver anslutning
        for btn in self.advanced_tab.findChildren(QPushButton) + \
                   self.raw_tab.findChildren(QPushButton) + \
                   self.config_tab.findChildren(QPushButton):
            btn.setEnabled(is_enabled)


    def reset_device(self):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(bytes([0x1B, 0x61]))
                self.log_message(self.strings["device_reset"])
            except Exception as e:
                self.log_message(self.strings["reset_error"].format(str(e)))
    
    def send_command(self, command, description, expect_response=True, timeout=10):
        if not self.is_connected:
            QMessageBox.critical(self, self.strings["error"], self.strings["not_connected"])
            return None
        
        try:
            self.ser.write(command)
            self.log_message(self.strings["command_sent"].format(description))
            QApplication.processEvents() # Håller UI:t responsivt
            
            if not expect_response: return None
                
            start_time = time.time()
            response = b""
            while time.time() - start_time < timeout:
                if self.ser.in_waiting:
                    response += self.ser.read(self.ser.in_waiting)
                    if len(response) >= 2 and response[-2] == 0x1B: break
                time.sleep(0.05)
                QApplication.processEvents()
            
            if response: return response
            else:
                self.log_message(self.strings["timeout"].format(description))
                return None
                
        except Exception as e:
            self.log_message(self.strings["command_error"].format(description, str(e)))
            return None

    def read_card(self):
        response = self.send_command(bytes([0x1B, 0x72]), self.strings["read_card"], timeout=15)
        if response: self.process_read_response(response)

    def process_read_response(self, response):
        try:
            if response[0:2] != bytes([0x1B, 0x73]):
                self.log_message(self.strings["invalid_response"])
                return
            
            tracks = {1: "", 2: "", 3: ""}
            parts = response.split(b'\x1b')[1:]
            for part in parts:
                if not part: continue
                track_num = part[0]
                data = part[1:].split(b'?')[0]
                if track_num == 0x01: tracks[1] = data.decode(errors='ignore')
                elif track_num == 0x02: tracks[2] = data.decode(errors='ignore')
                elif track_num == 0x03: tracks[3] = data.decode(errors='ignore')

            self.update_track_data(tracks)
            
            status_byte = response[-1]
            if status_byte == 0x30: self.log_message(self.strings["read_success"])
            else: self.log_message(self.strings["read_error"].format(hex(status_byte)))
        except Exception as e:
            self.log_message(self.strings["process_error"].format(str(e)))

    def update_track_data(self, tracks):
        self.track1_edit.setText(tracks.get(1, ''))
        self.track2_edit.setText(tracks.get(2, ''))
        self.track3_edit.setText(tracks.get(3, ''))

    def write_card(self):
        if not any([self.track1_check.isChecked(), self.track2_check.isChecked(), self.track3_check.isChecked()]):
            QMessageBox.warning(self, self.strings["warning"], self.strings["select_track_to_write_warning"])
            return
        
        data_block = bytearray([0x1B, 0x73])
        if self.track1_check.isChecked() and self.track1_edit.text(): data_block += b'\x1b\x01' + self.track1_edit.text().encode()
        if self.track2_check.isChecked() and self.track2_edit.text(): data_block += b'\x1b\x02' + self.track2_edit.text().encode()
        if self.track3_check.isChecked() and self.track3_edit.text(): data_block += b'\x1b\x03' + self.track3_edit.text().encode()
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
        if self.track1_check.isChecked(): select_byte |= 0x01
        if self.track2_check.isChecked(): select_byte |= 0x02
        if self.track3_check.isChecked(): select_byte |= 0x04
        
        if select_byte == 0:
            QMessageBox.warning(self, self.strings["warning"], self.strings["select_track_to_erase_warning"])
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
            
            self.update_raw_track_data(tracks)
            
            status_byte = response[-1]
            if status_byte == 0x30: self.log_message(self.strings["raw_read_success"])
            else: self.log_message(self.strings["raw_read_error"].format(hex(status_byte)))
        except Exception as e:
            self.log_message(self.strings["process_error"].format(str(e)))

    def update_raw_track_data(self, tracks):
        self.raw_track1_edit.setText(tracks.get(1, ''))
        self.raw_track2_edit.setText(tracks.get(2, ''))
        self.raw_track3_edit.setText(tracks.get(3, ''))

    def write_raw_data(self):
        data_block = bytearray([0x1B, 0x73])
        try:
            if self.raw_track1_edit.text():
                raw = bytes.fromhex(self.raw_track1_edit.text())
                data_block += bytes([0x1B, 0x01, len(raw)]) + raw
            if self.raw_track2_edit.text():
                raw = bytes.fromhex(self.raw_track2_edit.text())
                data_block += bytes([0x1B, 0x02, len(raw)]) + raw
            if self.raw_track3_edit.text():
                raw = bytes.fromhex(self.raw_track3_edit.text())
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
            lz_13 = int(self.leading_zero_13_edit.text())
            lz_2 = int(self.leading_zero_2_edit.text())
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
            cmd1 = bytes([0x1B, 0x62, bpi_map[self.bpi_track1_combo.currentText()]])
            
            bpi_map_t2 = {"75": 0x4B, "210": 0xD2}
            cmd2 = bytes([0x1B, 0x62, bpi_map_t2[self.bpi_track2_combo.currentText()]])
            
            bpi_map_t3 = {"75": 0xC0, "210": 0xC1}
            cmd3 = bytes([0x1B, 0x62, bpi_map_t3[self.bpi_track3_combo.currentText()]])
            
            for cmd, track, bpi_val in [(cmd1, self.strings["track1"][:-1], self.bpi_track1_combo.currentText()),
                                        (cmd2, self.strings["track2"][:-1], self.bpi_track2_combo.currentText()),
                                        (cmd3, self.strings["track3"][:-1], self.bpi_track3_combo.currentText())]:
                response = self.send_command(cmd, f"Set BPI for {track}")
                if response == b'\x1b\x30': self.log_message(self.strings["bpi_set_success"].format(track, bpi_val))
                elif response: self.log_message(self.strings["bpi_set_fail"].format(track, response.hex()))
        except Exception as e:
            self.log_message(self.strings["bpi_set_error"].format(str(e)))

    def set_bpc(self):
        try:
            bpc1 = int(self.bpc_track1_combo.currentText())
            bpc2 = int(self.bpc_track2_combo.currentText())
            bpc3 = int(self.bpc_track3_combo.currentText())
            if not (5 <= bpc1 <= 8 and 5 <= bpc2 <= 8 and 5 <= bpc3 <= 8): raise ValueError()
            
            command = bytes([0x1B, 0x6F, bpc1, bpc2, bpc3])
            response = self.send_command(command, self.strings["set_bpc"])
            
            if response and len(response) == 5 and response[:2] == b'\x1b\x30':
                self.log_message(self.strings["bpc_set_success"].format(response[2], response[3], response[4]))
            elif response: self.log_message(self.strings["bpc_set_fail"].format(response.hex()))
        except ValueError:
            self.log_message(self.strings["invalid_bpc_value"])
            
    def set_coercivity(self):
        cmd_code = 0x78 if self.high_co_radio.isChecked() else 0x79
        response = self.send_command(bytes([0x1B, cmd_code]), self.strings["set_coercivity"])
        if response == b'\x1b\x30':
            co_text = self.strings["high_co"] if self.high_co_radio.isChecked() else self.strings["low_co"]
            self.log_message(self.strings["coercivity_set_success"].format(co_text))
        elif response: self.log_message(self.strings["coercivity_set_fail"].format(response.hex()))

    def generate_card(self):
        card_type = self.card_type_combo.currentText()
        bin_number = self.bin_edit.text().strip()
        card_number = self.generate_card_number(card_type, bin_number)
        if not card_number: return
        
        expiry_date = self.generate_expiry_date()
        cvv = self.generate_cvv(card_type)
        
        self.card_number_edit.setText(card_number)
        self.card_expiry_edit.setText(expiry_date)
        self.card_cvv_edit.setText(cvv)
        
        self.log_message(self.strings["card_generated"].format(card_type, card_number))

    def generate_card_number(self, card_type, bin_number=""):
        s = self.strings
        if bin_number:
            if len(bin_number) != 6 or not bin_number.isdigit():
                QMessageBox.critical(self, s["error"], s["invalid_bin_error"])
                return ""
            
            warnings = {
                "Visa": (not bin_number.startswith("4"), s["bin_mismatch_warning_visa"]),
                "Mastercard": (not any(bin_number.startswith(p) for p in ("51", "52", "53", "54", "55", "22", "23", "24", "25", "26", "27")), s["bin_mismatch_warning_mastercard"]),
                "American Express": (not bin_number.startswith(("34", "37")), s["bin_mismatch_warning_amex"]),
                "Diners Club": (not bin_number.startswith(("36", "38", "39")), s["bin_mismatch_warning_diners"])
            }
            if card_type in warnings and warnings[card_type][0]:
                reply = QMessageBox.question(self, s["warning"], warnings[card_type][1],
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.No:
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
        return random_date.strftime("%y%m") # YYMM format för spår

    def generate_cvv(self, card_type):
        return str(random.randint(1000, 9999)) if card_type == "American Express" else str(random.randint(100, 999))

    def copy_to_track1(self):
        card_number = self.card_number_edit.text()
        expiry_date = self.card_expiry_edit.text() # YYMM
        card_holder = "TEST/CARDHOLDER"
        track1_data = f"%B{card_number}^{card_holder}^{expiry_date}101?"
        self.track1_edit.setText(track1_data)
        self.log_message(self.strings["copied_to_track1"])

    def copy_to_track2(self):
        card_number = self.card_number_edit.text()
        expiry_date = self.card_expiry_edit.text() # YYMM
        track2_data = f";{card_number}={expiry_date}101?"
        self.track2_edit.setText(track2_data)
        self.log_message(self.strings["copied_to_track2"])

    def copy_to_both_tracks(self):
        self.copy_to_track1()
        self.copy_to_track2()
        self.log_message(self.strings["copied_to_both"])

    def log_message(self, message):
        timestamp = time.strftime('%H:%M:%S')
        self.log_text.append(f"{timestamp} - {message}")
        self.log_text.moveCursor(QTextCursor.MoveOperation.End)

    def closeEvent(self, event):
        """Säkerställer att serieporten stängs när fönstret stängs."""
        self.disconnect_serial()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MSRE206_Qt_App()
    window.show()
    sys.exit(app.exec())
