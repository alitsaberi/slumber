from PySide6.QtWidgets import QMainWindow, QSizePolicy, QLabel, QPushButton, QTableView, QComboBox, QLCDNumber, QListWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from .main_window_ui import Ui_MainWindow
from .pages.settings.settings import SettingsPage
from .pages.help.help import HelpPage
from .pages.home.home import HomePage
from .pages.procedure.procedure import ProcedurePage
from .pages.thank_you.thank_you import ThankYouPage
from model.gui_config_model import get_gui_config
from model.task_progress_model import get_diary

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, gui_config, study_config, tasks, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)  # Setup the UI from the generated class

        self.home_page = HomePage(self)
        self.settings_page = SettingsPage(gui_config, self)
        self.help_page = HelpPage(self)
        self.procedure_page = ProcedurePage(tasks, self)
        self.thank_you_page = ThankYouPage(self)
        
        self.home_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.settings_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.help_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.procedure_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.thank_you_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.stackedWidgetPages.addWidget(self.home_page)
        self.stackedWidgetPages.addWidget(self.settings_page)
        self.stackedWidgetPages.addWidget(self.help_page)
        self.stackedWidgetPages.addWidget(self.procedure_page)
        self.stackedWidgetPages.addWidget(self.thank_you_page)

        self.stackedWidgetPages.setCurrentWidget(self.home_page) 

        self.pushButton_help.clicked.connect(self.on_help_button_clicked)
        self.pushButton_settings.clicked.connect(self.on_settings_button_clicked)

        # Connect the config_changed signal and config_back signal from the settings window
        self.settings_page.config_changed_signal.connect(self.on_config_changed)
        self.settings_page.config_back_signal.connect(self.go_back_pressed)

        # Connect the help_back signal from the help page
        self.help_page.help_back_signal.connect(self.go_back_pressed)

        # Connect the start_procedure signal from the home page
        self.home_page.pushButton_start_procedure.clicked.connect(self.on_start_procedure_clicked)

        # Connect the procedure_completed signal from the procedure page
        self.procedure_page.procedure_completed_signal.connect(self.on_procedure_completed)

        # Connect the thank_you_back signal from the thank you page
        self.thank_you_page.thank_you_back_signal.connect(self.go_back_after_thank_you)

        # Store the original default font sizes
        self.default_font_sizes = {}
        self.store_default_font_sizes()

        self.update_gui_config(gui_config)

        # Check if procedure is already started
        self.procedure_started = False

        

    def store_default_font_sizes(self):
        for widget in self.findChildren(QLabel):
            self.default_font_sizes[widget] = widget.font().pointSize()

        for widget in self.findChildren(QPushButton):
            self.default_font_sizes[widget] = widget.font().pointSize()

        for widget in self.findChildren(QTableView):
            self.default_font_sizes[widget] = widget.font().pointSize()

        for widget in self.findChildren(QComboBox):
            self.default_font_sizes[widget] = widget.font().pointSize()

        for widget in self.findChildren(QLCDNumber):
            self.default_font_sizes[widget] = widget.font().pointSize()

        for widget in self.findChildren(QWebEngineView):
            self.default_font_sizes[widget] = 1.0 

        for widget in self.findChildren(QListWidget):
            self.default_font_sizes[widget] = widget.font().pointSize()


    def on_start_procedure_clicked(self):
        print("Start Procedure button pressed")
        self.procedure_started = True
        self.stackedWidgetPages.setCurrentWidget(self.procedure_page)

    def on_help_button_clicked(self):
        print("Help button pressed")
        self.stackedWidgetPages.setCurrentWidget(self.help_page)

    def on_settings_button_clicked(self):
        print("Settings button pressed")
        self.stackedWidgetPages.setCurrentWidget(self.settings_page)

    def disable_buttons(self):
        self.pushButton_help.setEnabled(False)
        self.pushButton_settings.setEnabled(False)

    def enable_buttons(self):
        self.pushButton_help.setEnabled(True)
        self.pushButton_settings.setEnabled(True)

    def on_config_changed(self):
        print("Config updated")
        self.update_gui_config(get_gui_config())

    def go_back_pressed(self):
        print("Config back")
        if self.procedure_started:
            self.stackedWidgetPages.setCurrentWidget(self.procedure_page)
        else:
            self.stackedWidgetPages.setCurrentWidget(self.home_page)

    def go_back_after_thank_you(self):
        print("Back after thank you")
        self.stackedWidgetPages.setCurrentWidget(self.home_page)
        # Set start procudure button to close application
        self.home_page.pushButton_start_procedure.setText("Close Application")
        self.home_page.pushButton_start_procedure.clicked.disconnect()
        self.home_page.pushButton_start_procedure.clicked.connect(self.close)

    def update_gui_config(self, gui_config):
        font_size = gui_config['font_size']
        
        # Update font sizes for different widget types
        for widget in self.findChildren(QLabel):
            font = widget.font()
            default_font_size = self.default_font_sizes[widget]
            font.setPointSize(default_font_size + font_size)
            widget.setFont(font)

        for widget in self.findChildren(QPushButton):
            font = widget.font()
            default_font_size = self.default_font_sizes[widget]
            font.setPointSize(default_font_size + font_size)
            widget.setFont(font)

        for widget in self.findChildren(QTableView):
            font = widget.font()
            default_font_size = self.default_font_sizes[widget]
            font.setPointSize(default_font_size + font_size)
            widget.setFont(font)

        for widget in self.findChildren(QComboBox):
            font = widget.font()
            default_font_size = self.default_font_sizes[widget]
            font.setPointSize(default_font_size + font_size)
            widget.setFont(font)

        for widget in self.findChildren(QLCDNumber):
            font = widget.font()
            default_font_size = self.default_font_sizes[widget]
            font.setPointSize(default_font_size + font_size)
            widget.setFont(font)

        for widget in self.findChildren(QWebEngineView):
            default_zoom_factor = self.default_font_sizes[widget]
            widget.setZoomFactor(default_zoom_factor + (font_size * 0.1))  # Adjust zoom factor based on font size

        for widget in self.findChildren(QListWidget):
            font = widget.font()
            default_font_size = self.default_font_sizes[widget]
            font.setPointSize(default_font_size + font_size)
            widget.setFont(font)

        # Change main window size
        if gui_config['app_mode'] == 'full_screen':
            self.showFullScreen()
        else:
            self.showNormal()
            self.resize(gui_config['app_width'], gui_config['app_height'])

    def on_procedure_completed(self):
        print("Procedure completed")
        self.stackedWidgetPages.setCurrentWidget(self.thank_you_page)
