from PySide6.QtCore import QSize, Signal
from PySide6.QtWidgets import QDialog, QPushButton, QWidget

from .help_ui import Ui_HelpDialog
from .widget_ui import Ui_Widget


class WidgetPage(QWidget, Ui_Widget):
    is_done_signal = Signal(int)

    # Getting a index as well as status parameter to set the status of the task
    # 1: Task is not done
    # 2: Task is done
    def __init__(self, index, status=1, parent=None):
        super().__init__(parent)
        self.index = index
        self.status = status
        self.setupUi(self)  # Setup the UI from the generated class

        # Connect the info button to open the help dialog
        self.button_info.clicked.connect(self.open_help_dialog)

        # TODO: DELETE THIS BUTTON
        self.button_done = QPushButton("Done", self)
        self.button_done.setObjectName("button_done")
        self.button_done.setMinimumSize(QSize(100, 40))
        self.verticalLayout.addWidget(self.button_done)
        self.button_done.clicked.connect(self.emit_done_signal)

    def start(self):
        # TODO: Implement your functionality here, which will be called when the
        # task opens.
        # Make sure to use the status as well, to make sure to not call this
        # function several times
        if self.status == 1:
            print("Task started")
        else:
            print("Task already done")

    def open_help_dialog(self):
        # Create a QDialog instance
        dialog = QDialog(self)
        dialog.setWindowTitle("Help")  # Optional: Set window title

        # Set up the UI for the dialog using Ui_HelpDialog
        ui = Ui_HelpDialog()
        ui.setupUi(dialog)

        # Connect dialog buttons to methods
        # Assuming your help.ui has buttons named 'button_ok' and 'button_cancel'
        ui.button_ok.clicked.connect(
            lambda: self.handle_help_response(dialog, accepted=True)
        )
        ui.button_cancel.clicked.connect(
            lambda: self.handle_help_response(dialog, accepted=False)
        )

        # Execute the dialog modally
        dialog.exec()

    def handle_help_response(self, dialog, accepted):
        if accepted:
            print("OK button pressed in Help Dialog")
        else:
            print("Cancel button pressed in Help Dialog")
        # Close the dialog
        dialog.close()

    # DELETE THIS FUNCTION
    def emit_done_signal(self):
        if self.status == 1:
            self.is_done_signal.emit(self.index)
        self.status = 2
