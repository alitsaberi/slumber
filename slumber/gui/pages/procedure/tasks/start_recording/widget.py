from PySide6.QtWidgets import QWidget, QDialog
from PySide6.QtCore import Signal
from .help_ui import Ui_HelpDialog
from .widget_ui import Ui_Widget
import os

class WidgetPage(QWidget, Ui_Widget):
    is_done_signal = Signal()

    def __init__(self, parent=None):
        super(WidgetPage, self).__init__(parent)
        self.setupUi(self)  # Setup the UI from the generated class

        # Connect the info button to open the help dialog
        self.button_info.clicked.connect(self.open_help_dialog)

    def open_help_dialog(self):
        # Create a QDialog instance
        dialog = QDialog(self)
        dialog.setWindowTitle("Help")  # Optional: Set window title

        # Set up the UI for the dialog using Ui_HelpDialog
        ui = Ui_HelpDialog()
        ui.setupUi(dialog)

        # Connect dialog buttons to methods
        # Assuming your help.ui has buttons named 'button_ok' and 'button_cancel'
        ui.button_ok.clicked.connect(lambda: self.handle_help_response(dialog, accepted=True))
        ui.button_cancel.clicked.connect(lambda: self.handle_help_response(dialog, accepted=False))

        # Execute the dialog modally
        dialog.exec()

    def handle_help_response(self, dialog, accepted):
        if accepted:
            print("OK button pressed in Help Dialog")
        else:
            print("Cancel button pressed in Help Dialog")
        
        # Emit the signal to notify that the help dialog has been handled
        self.is_done_signal.emit()

        # Close the dialog
        dialog.close()