from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget

from ....model.gui_config_model import update_gui_config
from .settings_ui import Ui_SettingsWindow


class SettingsPage(QWidget, Ui_SettingsWindow):
    config_changed_signal = Signal()
    config_back_signal = Signal()

    def __init__(self, gui_config, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Setup the UI from the generated class

        self.gui_config = gui_config
        # Keep a copy of the original config to compare changes
        self.original_config = gui_config.copy()
        self.load_config()

        self.settings_back.clicked.connect(self.on_back_button_clicked)
        self.pushButton_font_size_dec.clicked.connect(self.on_font_size_decr_clicked)
        self.pushButton_font_size_add.clicked.connect(self.on_font_size_add_clicked)
        self.settings_save.clicked.connect(self.on_save_button_clicked)

        self.comboBox_size.currentIndexChanged.connect(self.on_size_changed)
        self.comboBox_window_mode.currentIndexChanged.connect(self.on_window_mode_changed)
        self.comboBox_language.currentIndexChanged.connect(self.on_language_changed)

    def load_config(self):
        if self.gui_config:
            print(self.gui_config)
            
            # Update lcdNumber_font_size
            self.lcdNumber_font_size.display(self.gui_config['font_size'])
            self.update_font_size_buttons()

            # Update comboBox_language
            index = self.comboBox_language.findText(
                self.gui_config['language'], Qt.MatchFixedString)
            if index >= 0:
                self.comboBox_language.setCurrentIndex(index)

            # Update comboBox_window_mode
            mode = "Window" if self.gui_config['app_mode'] == 'window' else \
                "Full Screen"
            index = self.comboBox_window_mode.findText(mode, Qt.MatchFixedString)
            if index >= 0:
                self.comboBox_window_mode.setCurrentIndex(index)

            # Update comboBox_size
            size_map = {
                (1600, 900): "1600x900 (HD+)",
                (1680, 1050): "1680x1050 (WSXGA+)",
                (1920, 1080): "1920x1080 (Full HD)",
                (1920, 1200): "1920x1200 (WUXGA)",
                (2560, 1440): "2560x1440 (QHD)",
                (2560, 1600): "2560x1600 (WQXGA)",
                (3840, 2160): "3840x2160 (4K UHD)",
                (4096, 2160): "4096x2160 (4K DCI)"
            }
            size_text = size_map.get(
                (self.gui_config['app_width'], self.gui_config['app_height']), 
                ""
            )
            index = self.comboBox_size.findText(size_text, Qt.MatchFixedString)
            if index >= 0:
                self.comboBox_size.setCurrentIndex(index)

    def update_font_size_buttons(self):
        font_size = self.lcdNumber_font_size.intValue()
        self.pushButton_font_size_dec.setEnabled(font_size > 0)
        self.pushButton_font_size_add.setEnabled(font_size < 9)

    def check_for_changes(self):
        current_config = {
            'font_size': self.lcdNumber_font_size.intValue(),
            'language': self.comboBox_language.currentText(),
            'app_mode': 'window' if self.comboBox_window_mode.currentText() == 'Window' 
                        else 'full_screen',
            'app_width': int(self.comboBox_size.currentText().split('x')[0]),
            'app_height': int(
                self.comboBox_size.currentText().split('x')[1].split(' ')[0]
            )
        }
        self.settings_save.setEnabled(current_config != self.original_config)

    def on_back_button_clicked(self):
        print("Back button pressed")
        self.config_back_signal.emit()

    def on_font_size_decr_clicked(self):
        print("Font size decrease button pressed")
        font_size = self.lcdNumber_font_size.intValue()
        if font_size > 0:
            font_size -= 1
            self.lcdNumber_font_size.display(font_size)
            self.update_font_size_buttons()
            self.check_for_changes()

    def on_font_size_add_clicked(self):
        print("Font size increase button pressed")
        font_size = self.lcdNumber_font_size.intValue()
        if font_size < 9:
            font_size += 1
            self.lcdNumber_font_size.display(font_size)
            self.update_font_size_buttons()
            self.check_for_changes()

    def on_save_button_clicked(self):
        print("Save button pressed")
        current_config = {
            'font_size': self.lcdNumber_font_size.intValue(),
            'language': self.comboBox_language.currentText(),
            'app_mode': 'window' if self.comboBox_window_mode.currentText() == 'Window' 
                        else 'full_screen',
            'app_width': int(self.comboBox_size.currentText().split('x')[0]),
            'app_height': int(
                self.comboBox_size.currentText().split('x')[1].split(' ')[0]
            )
        }
        update_gui_config(
            current_config['font_size'],
            current_config['app_width'],
            current_config['app_height'],
            current_config['app_mode'],
            current_config['language']
        )
        self.original_config = current_config.copy()
        self.settings_save.setEnabled(False)
        self.config_changed_signal.emit()

    def on_size_changed(self, index):
        size = self.comboBox_size.itemText(index)
        print(f"Size changed to: {size}")
        self.check_for_changes()

    def on_window_mode_changed(self, index):
        mode = self.comboBox_window_mode.itemText(index)
        print(f"Window mode changed to: {mode}")
        self.check_for_changes()

    def on_language_changed(self, index):
        language = self.comboBox_language.itemText(index)
        print(f"Language changed to: {language}")
        self.check_for_changes()