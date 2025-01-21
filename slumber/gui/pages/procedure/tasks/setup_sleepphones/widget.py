import asyncio
import os

from bleak import BleakClient, BleakError, BleakScanner
from PySide6.QtCore import QSize, QTimer, QUrl, Signal
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QDialog, QListWidgetItem, QPushButton, QWidget

from .help_ui import Ui_HelpDialog
from .widget_ui import Ui_Widget


class WidgetPage(QWidget, Ui_Widget):
    """
    Example widget that scans Bluetooth devices asynchronously using Bleak.
    This code assumes that the main PySide6 application event loop is integrated
    with asyncio via qasync, so `asyncio.create_task()` will work without errors.
    """
    is_done_signal = Signal(int)
    bluetooth_status = False
    is_connected = False

    def __init__(self, index, status=1, parent=None):
        super().__init__(parent)
        self.index = index
        self.status = status
        self.connected_client = None
        self.setupUi(self)  # Setup the UI from the generated .ui file

        # Connect the info button to open the help dialog
        self.button_info.clicked.connect(self.open_help_dialog)

         # Load the HTML file into the QWebEngineView
        html_file_path = os.path.join(os.path.dirname(__file__), 'assets/html/index.html')
        self.webEngineView_sleep_phones.setUrl(QUrl.fromLocalFile(html_file_path))

        # Connect the refresh button to scan for Bluetooth devices
        self.button_refresh.clicked.connect(self.scan_bluetooth_devices)

        # 2) Listen for double-clicks on the list to trigger connection
        self.list_bluetooth_devices.itemDoubleClicked.connect(self.on_device_double_clicked)

        # Example "Done" button (not in your .ui, but added programmatically)
        self.button_done = QPushButton("Done", self)
        self.button_done.setObjectName("button_done")
        self.button_done.setMinimumSize(QSize(100, 40))
        self.verticalLayout.addWidget(self.button_done)
        self.button_done.clicked.connect(self.emit_done_signal)

        # Check Bluetooth status on initialization
        # SingleShot(0, ...) schedules this check right after the widget is shown
        QTimer.singleShot(0, self.start_check_bluetooth_status)

        # 4) Check if we are already connected (example: if your app reuses
        #    a BleakClient from a prior step). For this demo, it's just a 
        #    placeholder call:
        self.check_if_already_connected()

        # 5) Hook the radio button's "toggled" signal to color text green if checked
        self.radio_status.toggled.connect(self.on_radio_status_toggled)

    def start_check_bluetooth_status(self):
        asyncio.create_task(self.perform_bluetooth_initialization())

    def start(self):
        if self.status == 1:
            print("Task started")
        else:
            print("Task already done")

    def open_help_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Help")

        ui = Ui_HelpDialog()
        ui.setupUi(dialog)

        ui.button_ok.clicked.connect(
            lambda: self.handle_help_response(dialog, accepted=True)
        )
        ui.button_cancel.clicked.connect(
            lambda: self.handle_help_response(dialog, accepted=False)
        )

        dialog.exec()

    def handle_help_response(self, dialog, accepted):
        if accepted:
            print("OK button pressed in Help Dialog")
        else:
            print("Cancel button pressed in Help Dialog")
        dialog.close()

    def emit_done_signal(self):
        if self.status == 1:
            self.is_done_signal.emit(self.index)
        self.status = 2

    async def async_scan_bluetooth_devices(self):
        """Asynchronously discover BLE devices, then populate the list widget."""
        self.radio_status.setText("Status: Loading...")
        self.list_bluetooth_devices.clear()  # Clear the list before scanning

        try:
            # Perform async BLE scan
            devices = await BleakScanner.discover()

            # Filter out devices with no name
            named_devices = [
                d for d in devices if d.name
            ]  # Keep only those with a non-empty name

            # Populate the list with named devices
            for device in named_devices:
                item = QListWidgetItem(f"{device.name} ({device.address})")
                self.list_bluetooth_devices.addItem(item)

            # Update the status label based on how many named devices were found
            count_named = len(named_devices)
            if count_named > 0:
                self.radio_status.setText(f"Status: Found {count_named} devices")
            else:
                self.radio_status.setText("Status: No devices found")

        except BleakError as e:
            # On error, show the error text
            self.radio_status.setText(f"Status: Error ({str(e)})")

    def scan_bluetooth_devices(self):
        """
        This slot is called when the refresh button is clicked.
        We show 'loading' text and then schedule the async scan.
        """
        # 1) Set the radio_status text to indicate scanning/ loading
        self.radio_status.setText("Status: Loading...")

        # 2) Kick off the async scan in the background
        asyncio.create_task(self.async_scan_bluetooth_devices())

    async def check_bluetooth_status(self):
        """Async check of whether Bluetooth is 'on' or 'off' (heuristic)."""
        if self.bluetooth_status:
            self.button_refresh.setEnabled(True)
        else:
            self.radio_status.setText("Status: Bluetooth is off or no devices found")
            self.button_refresh.setEnabled(False)

    async def is_bluetooth_on(self):
        """
        A simple check: tries to discover devices. If Bleak can find
        something, we treat it as 'Bluetooth on.'
        """
        try:
            devices = await BleakScanner.discover()
            return bool(devices)  # True if any devices found
        except BleakError:
            # BleakError can happen if the adapter is not available or off
            return False
        

    def on_device_double_clicked(self, item):
        """
        Triggered when the user double-clicks on a device in the list.
        We attempt to connect to that device.
        """
        asyncio.create_task(self.async_connect_to_device(item.text()))

    async def async_connect_to_device(self, device_text):
        """
        Parse device address from the item text,
        attempt to connect using Bleak.
        """
        # Example: item_text = "My Headphones (AA:BB:CC:DD:EE:FF)"
        # We'll parse out the address in parentheses:
        address = self._parse_device_address(device_text)
        if not address:
            self.radio_status.setText("Status: Invalid address")
            return

        self.radio_status.setText("Status: Connecting...")
        self.radio_status.setChecked(False)
        self.radio_status.setStyleSheet("")  # default color

        # If we already have a client, disconnect first (optional)
        if self.connected_client and self.connected_client.is_connected:
            import contextlib
            with contextlib.suppress(Exception):
                await self.connected_client.disconnect()
            self.connected_client = None

        # Attempt new connection
        try:
            client = BleakClient(address)
            await client.connect()
            if client.is_connected:
                # Mark as connected
                self.connected_client = client
                self.radio_status.setText("Status: Connected")
                self.radio_status.setChecked(True)
                # Make text green if radio is checked:
                self.radio_status.setStyleSheet("color: green;")
                # Emit signal if you want to indicate "Done" or "Connected"
                self.is_done_signal.emit(self.index)
            else:
                self.radio_status.setText("Status: Could not connect")
        except BleakError as e:
            self.radio_status.setText(f"Status: Error connecting ({str(e)})")

    def _parse_device_address(self, item_text: str) -> str:
        """
        Helper function to extract the BLE address from item text like
        'My Device (12:34:56:78:9A:BC)'. 
        Returns None if not found.
        """
        import re
        match = re.search(r"\(([^)]+)\)", item_text)
        if match:
            return match.group(1).strip()
        return None

    def check_if_already_connected(self):
        """
        Placeholder. If your app logic knows you're already connected to a device
        or re-uses an existing BleakClient, you can check that here.
        Then set the status to "Connected", etc.
        """
        if self.connected_client and self.connected_client.is_connected:
            self.radio_status.setText("Status: Connected")
            self.radio_status.setChecked(True)
            self.radio_status.setStyleSheet("color: green;")
            self.is_done_signal.emit(self.index)
        else:
            # Not connected
            self.radio_status.setText("Status")
            self.radio_status.setChecked(False)
            self.radio_status.setStyleSheet("")

    def on_radio_status_toggled(self, checked: bool):
        if checked:
            self.radio_status.setStyleSheet("color: green;")
        else:
            self.radio_status.setStyleSheet("")

    async def perform_bluetooth_initialization(self):
        self.bluetooth_status = 1 if await self.is_bluetooth_on() else 0
        await self.check_bluetooth_status()
        await self.async_scan_bluetooth_devices()