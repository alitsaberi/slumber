from loguru import logger
from PySide6.QtWidgets import (
    QMainWindow,
)

from .main_window_ui import Ui_main_window


class MainWindow(QMainWindow, Ui_main_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Setup the UI from the generated class

        # self.home_page = HomePage(self)
        # self.settings_page = SettingsPage(gui_config, self)
        # self.help_page = HelpPage(self)
        # self.procedure_page = ProcedurePage(tasks, self)

        # self.home_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.settings_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.help_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.procedure_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.thank_you_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # self.stackedWidgetPages.addWidget(self.home_page)
        # self.stackedWidgetPages.addWidget(self.settings_page)
        # self.stackedWidgetPages.addWidget(self.help_page)
        # self.stackedWidgetPages.addWidget(self.procedure_page)
        # self.stackedWidgetPages.addWidget(self.thank_you_page)

        # self.stackedWidgetPages.setCurrentWidget(self.home_page)

        # self.pushButton_help.clicked.connect(self.on_help_button_clicked)
        # self.pushButton_settings.clicked.connect(self.on_settings_button_clicked)

        # Connect the config_changed signal and config_back signal
        # from the settings window
        # self.settings_page.config_changed_signal.connect(self.on_config_changed)
        # self.settings_page.config_back_signal.connect(self.go_back_pressed)

        # Connect the help_back signal from the help page
        # self.help_page.help_back_signal.connect(self.go_back_pressed)

        # Connect the start_procedure signal from the home page
        # self.home_page.pushButton_start_procedure.clicked.connect(
        #     self.on_start_procedure_clicked
        # )

        # Connect the procedure_completed signal from the procedure page
        # self.procedure_page.procedure_completed_signal.connect(
        #     self.on_procedure_completed
        # )

        # Connect the thank_you_back signal from the thank you page
        # self.thank_you_page.thank_you_back_signal.connect(self.go_back_after_thank_you)

        # Store the original default font sizes
        # self.default_font_sizes = {}
        # self.store_default_font_sizes()

        # self.update_gui_config(gui_config)

        # Check if procedure is already started
        # self.procedure_started = False

    # def store_default_font_sizes(self):
    #     for widget in self.findChildren(QLabel):
    #         self.default_font_sizes[widget] = widget.font().pointSize()

    #     for widget in self.findChildren(QPushButton):
    #         self.default_font_sizes[widget] = widget.font().pointSize()

    #     for widget in self.findChildren(QTableView):
    #         self.default_font_sizes[widget] = widget.font().pointSize()

    #     for widget in self.findChildren(QComboBox):
    #         self.default_font_sizes[widget] = widget.font().pointSize()

    #     for widget in self.findChildren(QLCDNumber):
    #         self.default_font_sizes[widget] = widget.font().pointSize()

    #     for widget in self.findChildren(QWebEngineView):
    #         self.default_font_sizes[widget] = 1.0

    #     for widget in self.findChildren(QListWidget):
    #         self.default_font_sizes[widget] = widget.font().pointSize()

    # def on_start_procedure_clicked(self):
    #     logger.info("Start Procedure button pressed")
    #     self.procedure_started = True
    #     self.stackedWidgetPages.setCurrentWidget(self.procedure_page)

    def on_help_button_clicked(self):
        logger.info("Help button pressed")
        # self.stacket.setCurrentWidget(self.help_page)

    def on_settings_button_clicked(self):
        logger.info("Settings button pressed")
        # self.stackedWidgetPages.setCurrentWidget(self.settings_page)

    def disable_buttons(self):
        self.help_button.setEnabled(False)
        self.settings_button.setEnabled(False)

    def enable_buttons(self):
        self.help_button.setEnabled(True)
        self.settings_button.setEnabled(True)

    # def on_config_changed(self):
    #     logger.info("Config updated")
    #     # self.update_gui_config(get_gui_config())

    def reset_central_widget(self):
        self.setCentralWidget(self.central_widget)
