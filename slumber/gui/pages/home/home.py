from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from .home_ui import Ui_HomePage
import os

class HomePage(QWidget, Ui_HomePage):
    def __init__(self, parent=None):
        super(HomePage, self).__init__(parent)
        self.setupUi(self)  # Setup the UI from the generated class

        self.pushButton_start_procedure.clicked.connect(self.on_start_procedure_clicked)

        # Load the HTML file
        html_file_path = os.path.join(os.path.dirname(__file__), './assets/html/index.html')
        self.webEngineView_main.setUrl(QUrl.fromLocalFile(html_file_path))

    def on_start_procedure_clicked(self):
        print("Start Procedure button pressed")