from PySide6.QtWidgets import QMainWindow
from .main_window_ui import Ui_MainWindow
from .pages.settings.settings import SettingsWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)  # Setup the UI from the generated class

        self.settings_window = SettingsWindow(self)
        self.stackedWidgetPages.addWidget(self.settings_window)

        self.pushButton_help.clicked.connect(self.on_help_button_clicked)
        self.pushButton_settings.clicked.connect(self.on_settings_button_clicked)

    def on_help_button_clicked(self):
        print("Help button pressed")

    def on_settings_button_clicked(self):
        print("Settings button pressed")
        self.stackedWidgetPages.setCurrentWidget(self.settings_window)

    def disable_buttons(self):
        self.pushButton_help.setEnabled(False)
        self.pushButton_settings.setEnabled(False)

    def enable_buttons(self):
        self.pushButton_help.setEnabled(True)
        self.pushButton_settings.setEnabled(True)