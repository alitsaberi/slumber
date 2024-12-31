from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QUrl, Signal
from PySide6.QtWebEngineWidgets import QWebEngineView
from .help_ui import Ui_HelpPage
import os

class HelpPage(QWidget, Ui_HelpPage):
    help_back_signal = Signal()

    def __init__(self, parent=None):
        super(HelpPage, self).__init__(parent)
        self.setupUi(self)  # Setup the UI from the generated class

        # Connect the back button to the help_back signal
        self.help_back.clicked.connect(self.on_back_button_clicked)

        # Load the HTML file
        html_file_path = os.path.join(os.path.dirname(__file__), './assets/html/index.html')
        self.webEngineView_help.setUrl(QUrl.fromLocalFile(html_file_path))

    def on_back_button_clicked(self):
        print("Back button pressed")
        self.help_back_signal.emit()