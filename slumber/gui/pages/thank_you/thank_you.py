from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QUrl, Signal
from PySide6.QtWebEngineWidgets import QWebEngineView
from .thank_you_ui import Ui_ThankYouPage
import os

class ThankYouPage(QWidget, Ui_ThankYouPage):
    thank_you_back_signal = Signal()

    def __init__(self, parent=None):
        super(ThankYouPage, self).__init__(parent)
        self.setupUi(self)  # Setup the UI from the generated class

        # Connect the back button to the help_back signal
        self.thank_you_back.clicked.connect(self.on_back_button_clicked)

        # Load the HTML file
        html_file_path = os.path.join(os.path.dirname(__file__), './assets/html/index.html')
        self.webEngineView_thank_you.setUrl(QUrl.fromLocalFile(html_file_path))

    def on_back_button_clicked(self):
        print("Back button pressed")
        self.thank_you_back_signal.emit()