# gui/main_window.py

from PySide6.QtWidgets import QMainWindow, QSizePolicy
from .main_window_ui import Ui_MainWindow
from .pages.settings.settings import SettingsWindow
from .pages.help.help import HelpPage
from .pages.home.home import HomePage

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)  # Setup the UI from the generated class

        self.home_page = HomePage(self)
        self.settings_window = SettingsWindow(self)
        self.help_page = HelpPage(self)
        
        self.home_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.settings_window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.help_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.stackedWidgetPages.addWidget(self.home_page)
        self.stackedWidgetPages.addWidget(self.settings_window)
        self.stackedWidgetPages.addWidget(self.help_page)

        self.stackedWidgetPages.setCurrentWidget(self.home_page) 

        self.pushButton_help.clicked.connect(self.on_help_button_clicked)
        self.pushButton_settings.clicked.connect(self.on_settings_button_clicked)

    def on_help_button_clicked(self):
        print("Help button pressed")
        self.stackedWidgetPages.setCurrentWidget(self.help_page)

    def on_settings_button_clicked(self):
        print("Settings button pressed")
        self.stackedWidgetPages.setCurrentWidget(self.settings_window)

    def disable_buttons(self):
        self.pushButton_help.setEnabled(False)
        self.pushButton_settings.setEnabled(False)

    def enable_buttons(self):
        self.pushButton_help.setEnabled(True)
        self.pushButton_settings.setEnabled(True)