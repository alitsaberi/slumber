import asyncio
import os

from bleak import BleakClient, BleakError, BleakScanner
from PySide6.QtCore import QTimer, QUrl, Signal
from PySide6.QtWidgets import QDialog, QListWidgetItem, QWidget

from .help_ui import Ui_HelpDialog
from .widget_ui import Ui_Widget


class WidgetPage(QWidget, Ui_Widget):
    """
    Widget for scanning and connecting to Bluetooth devices asynchronously using Bleak.
    Assumes integration with qasync for PySide6 event loop compatibility with asyncio.
    """
    is_done_signal = Signal(int)
    bluetooth_status = False
    is_connected = False

    def __init__(self, index, status=1, parent=None):
        super().__init__(parent)
        self.index = index  # Index identifier for the widget
        self.status = status  # Status indicator for the widget
        self.connected_client = None  # Placeholder for the connected Bluetooth client
        self.setupUi(self)  # Set up the UI components

        # Set up the help dialog button functionality
        self.button_info.clicked.connect(self.open_help_dialog)

        # Load the initial HTML file into the QWebEngineView
        html_file_path = os.path.join(os.path.dirname(__file__), 'assets/html/index.html')
        self.webEngineView_sleep_phones.setUrl(QUrl.fromLocalFile(html_file_path))

        # Connect the refresh button to the Bluetooth scanning functionality
        self.button_refresh.clicked.connect(self.scan_bluetooth_devices)

        # Handle double-clicks on the device list to initiate connection
        self.list_bluetooth_devices.itemDoubleClicked.connect(self.on_device_double_clicked)

        # Check Bluetooth status when the widget is initialized
        QTimer.singleShot(0, self.start_check_bluetooth_status)

        # Perform any checks for existing connections
        self.check_if_already_connected()

        # Set up the radio button toggling behavior
        self.radio_status.toggled.connect(self.on_radio_status_toggled)

    def start_check_bluetooth_status(self):
        """Start the Bluetooth status check asynchronously."""
        asyncio.create_task(self.perform_bluetooth_initialization())

    def start(self):
        """Start or indicate the status of a task based on the current widget state."""
        if self.status == 1:
            print("Task started")
        else:
            print("Task already done")

    def open_help_dialog(self):
        """Open a help dialog with basic information and options."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Help")

        ui = Ui_HelpDialog()
        ui.setupUi(dialog)

        # Connect dialog buttons to appropriate handlers
        ui.button_ok.clicked.connect(
            lambda: self.handle_help_response(dialog, accepted=True)
        )
        ui.button_cancel.clicked.connect(
            lambda: self.handle_help_response(dialog, accepted=False)
        )

        dialog.exec()

    def handle_help_response(self, dialog, accepted):
        """Handle the response from the help dialog."""
        if accepted:
            print("OK button pressed in Help Dialog")
        else:
            print("Cancel button pressed in Help Dialog")
        dialog.close()

    def emit_done_signal(self):
        """Emit a signal indicating the task is done."""
        if self.status == 1:
            self.is_done_signal.emit(self.index)
        self.status = 2

    async def async_scan_bluetooth_devices(self):
        """Scan for Bluetooth devices asynchronously and update the device list."""
        self.radio_status.setText("Status: Loading...")
        self.list_bluetooth_devices.clear()

        try:
            # Discover Bluetooth devices asynchronously
            devices = await BleakScanner.discover()

            # Filter and display devices with names
            named_devices = [d for d in devices if d.name]
            for device in named_devices:
                item = QListWidgetItem(f"{device.name} ({device.address})")
                self.list_bluetooth_devices.addItem(item)

            # Update status based on the number of devices found
            count_named = len(named_devices)
            if count_named > 0:
                self.radio_status.setText(f"Status: Found {count_named} devices")
            else:
                self.radio_status.setText("Status: No devices found")

        except BleakError as e:
            # Handle errors during scanning
            self.radio_status.setText(f"Status: Error ({str(e)})")

    def scan_bluetooth_devices(self):
        """Initiate scanning for Bluetooth devices."""
        self.radio_status.setText("Status: Loading...")
        asyncio.create_task(self.async_scan_bluetooth_devices())

    async def check_bluetooth_status(self):
        """Check whether Bluetooth is enabled and update the UI accordingly."""
        if self.bluetooth_status:
            self.button_refresh.setEnabled(True)
        else:
            self.radio_status.setText("Status: Bluetooth is off or no devices found")
            self.button_refresh.setEnabled(False)

    async def is_bluetooth_on(self):
        """Check if Bluetooth is on by attempting to discover devices."""
        try:
            devices = await BleakScanner.discover()
            return bool(devices)  # Return True if devices are found
        except BleakError:
            return False  # Handle errors as Bluetooth being off

    def on_device_double_clicked(self, item):
        """Handle a double-click event on a Bluetooth device to connect."""
        asyncio.create_task(self.async_connect_to_device(item.text()))

    async def async_connect_to_device(self, device_text):
        """Connect to the selected Bluetooth device asynchronously."""
        address = self._parse_device_address(device_text)
        if not address:
            self.radio_status.setText("Status: Invalid address")
            return

        self.radio_status.setText("Status: Connecting...")
        self.radio_status.setChecked(False)
        self.radio_status.setStyleSheet("")

        # Disconnect from any existing client before connecting
        if self.connected_client and self.connected_client.is_connected:
            import contextlib
            with contextlib.suppress(Exception):
                await self.connected_client.disconnect()
            self.connected_client = None

        try:
            # Attempt to connect to the new device
            client = BleakClient(address)
            await client.connect()
            if client.is_connected:
                self.connected_client = client
                self.radio_status.setText("Status: Connected")
                self.radio_status.setChecked(True)
                self.radio_status.setStyleSheet("color: green;")
                self.is_done_signal.emit(self.index)
            else:
                self.radio_status.setText("Status: Could not connect")
        except BleakError as e:
            self.radio_status.setText(f"Status: Error connecting ({str(e)})")

    def _parse_device_address(self, item_text: str) -> str:
        """Extract the Bluetooth address from the device text."""
        import re
        match = re.search(r"\(([^)]+)\)", item_text)
        if match:
            return match.group(1).strip()
        return None

    def check_if_already_connected(self):
        """Check and update the UI if already connected to a device."""
        if self.connected_client and self.connected_client.is_connected:
            self.radio_status.setText("Status: Connected")
            self.radio_status.setChecked(True)
            self.radio_status.setStyleSheet("color: green;")
            self.is_done_signal.emit(self.index)
        else:
            self.radio_status.setText("Status")
            self.radio_status.setChecked(False)
            self.radio_status.setStyleSheet("")

    def on_radio_status_toggled(self, checked: bool):
        """Change the text color based on the radio button status."""
        if checked:
            self.radio_status.setStyleSheet("color: green;")
        else:
            self.radio_status.setStyleSheet("")

    async def perform_bluetooth_initialization(self):
        """Perform initial Bluetooth setup and scan for devices."""
        self.bluetooth_status = 1 if await self.is_bluetooth_on() else 0
        await self.check_bluetooth_status()
        await self.async_scan_bluetooth_devices()
