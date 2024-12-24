from PySide6.QtWidgets import QWidget
from .settings_ui import Ui_SettingsWindow

class SettingsWindow(QWidget, Ui_SettingsWindow):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.setupUi(self)  # Setup the UI from the generated class

        self.settings_back.clicked.connect(self.on_back_button_clicked)
        self.pushButton_font_size_dec.clicked.connect(self.on_font_size_decr_clicked)
        self.pushButton_font_size_add.clicked.connect(self.on_font_size_add_clicked)
        self.pushButton_other_settings_add.clicked.connect(self.on_other_settings_add_clicked)
        self.pushButton_other_settings_dec.clicked.connect(self.on_other_settings_decr_clicked)
        self.settings_save.clicked.connect(self.on_save_button_clicked)

        self.comboBox_size.currentIndexChanged.connect(self.on_size_changed)
        self.comboBox_window_mode.currentIndexChanged.connect(self.on_window_mode_changed)

    def on_back_button_clicked(self):
        print("Back button pressed")

    def on_font_size_decr_clicked(self):
        print("Font size decrease button pressed")

    def on_font_size_add_clicked(self):
        print("Font size increase button pressed")

    def on_other_settings_add_clicked(self):
        print("Other settings add button pressed")

    def on_other_settings_decr_clicked(self):
        print("Other settings decrease button pressed")

    def on_save_button_clicked(self):
        print("Save button pressed")

    def on_size_changed(self, index):
        size = self.comboBox_size.itemText(index)
        print(f"Size changed to: {size}")

    def on_window_mode_changed(self, index):
        mode = self.comboBox_window_mode.itemText(index)
        print(f"Window mode changed to: {mode}")