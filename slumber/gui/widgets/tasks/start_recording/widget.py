import os
import random
from datetime import datetime

from PySide6.QtCore import QTimer, QUrl, Signal
from PySide6.QtMultimedia import QAudioOutput, QMediaMetaData, QMediaPlayer
from PySide6.QtWidgets import QDialog, QMessageBox, QWidget

from .help_ui import Ui_HelpDialog
from .widget_ui import Ui_Widget


class WidgetPage(QWidget, Ui_Widget):
    is_done_signal = Signal(int)

    def __init__(self, index, status=1, parent=None):
        super().__init__(parent)
        self.index = index
        self.status = status
        self.setupUi(self)

        self.button_info.clicked.connect(self.open_help_dialog)
        self.button_recording.clicked.connect(self.handle_recording)

        self.player_current = QMediaPlayer()
        self.audio_output_current = QAudioOutput()
        self.player_current.setAudioOutput(self.audio_output_current)
        self.audio_output_current.setVolume(1.0)

        self.player_next = QMediaPlayer()
        self.audio_output_next = QAudioOutput()
        self.player_next.setAudioOutput(self.audio_output_next)
        self.audio_output_next.setVolume(0.0)

        assets_path = os.path.join(os.path.dirname(__file__), "assets", "music")
        if not os.path.exists(assets_path):
            print(f"[WARNING] Assets path does not exist: {assets_path}")
            self.mp3_files = []
        else:
            self.mp3_files = [
                os.path.join(assets_path, file)
                for file in os.listdir(assets_path)
                if file.lower().endswith(".mp3")
            ]

        if not self.mp3_files:
            print(f"[WARNING] No MP3 files found in {assets_path}")
        else:
            print(f"[INFO] Loaded {len(self.mp3_files)} MP3 files.")

        self.current_song_index = 0
        self.next_song_index = 0

        self.player_current.mediaStatusChanged.connect(self.on_media_status_changed)
        self.player_next.mediaStatusChanged.connect(self.on_media_status_changed)
        self.player_current.positionChanged.connect(self.check_crossfade)

        self.crossfade_timer = QTimer()
        self.crossfade_timer.setInterval(100)
        self.crossfade_timer.timeout.connect(self.perform_crossfade)
        self.fade_duration = 10000
        self.fade_step = 0.05
        self.fading = False

        # Connect the metadataChanged signal for the current player
        self.player_current.metaDataChanged.connect(
            lambda: self.on_player_metadata_changed(self.player_current)
        )
        self.player_next.metaDataChanged.connect(
            lambda: self.on_player_metadata_changed(self.player_next)
        )

    def start(self):
        if self.status == 1:
            print(f"[INFO] Task started at {self.get_current_timestamp()}")
        else:
            print(f"[INFO] Task already done at {self.get_current_timestamp()}")

    def handle_recording(self):
        if self.button_recording.text() == "Start Recording":
            self.button_recording.setText("Stop Recording")
            self.button_recording.setStyleSheet("""
                QPushButton {
                    color: rgb(255, 255, 255);
                    background-color: rgb(255, 0, 0);
                    border: 1px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    color: rgb(220,221,229);
                    background-color: rgb(200, 0, 0);
                }
                QPushButton:pressed {
                    color: rgb(220,221,229);
                    background-color: rgb(200, 0, 0);
                }
                QPushButton:disabled {
                    color: rgb(190, 190, 190);
                    background-color: rgb(100, 100, 100);
                }
            """)
            print(f"[INFO] Recording started at {self.get_current_timestamp()}")
            if self.mp3_files:
                self.current_song_index = random.randint(0, len(self.mp3_files) - 1)
                self.play_current_song()
            else:
                print("[ERROR] No MP3 files to play.")
        else:
            reply = QMessageBox.warning(
                self,
                "Stop Recording",
                "Are you sure you want to stop recording?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                self.emit_done_signal()
                self.button_recording.setEnabled(False)
                self.player_current.stop()
                self.player_next.stop()
                print(f"[INFO] Recording stopped at {self.get_current_timestamp()}")

    def play_current_song(self):
        if not self.mp3_files:
            print("[WARNING] No MP3 files found in the assets/music folder.")
            return
        current_song = self.mp3_files[self.current_song_index]
        self.player_current.setSource(QUrl.fromLocalFile(current_song))
        self.player_current.play()

        print(f"[INFO] Playing: {current_song}")
        print(f"[INFO] Started at: {self.get_current_timestamp()}")

    def check_crossfade(self, position):
        duration = self.player_current.duration()
        if duration > 0 and not self.fading:
            remaining_time = duration - position
            if remaining_time <= self.fade_duration:
                self.start_crossfade()

    def start_crossfade(self):
        self.fading = True
        if not self.mp3_files:
            print("[ERROR] No MP3 files found for crossfade.")
            return
        self.next_song_index = random.randint(0, len(self.mp3_files) - 1)
        next_song = self.mp3_files[self.next_song_index]
        self.player_next.setSource(QUrl.fromLocalFile(next_song))
        self.player_next.play()
        print(f"[INFO] Playing next: {next_song}")
        print(f"[INFO] Next song started at: {self.get_current_timestamp()}")
        self.crossfade_timer.start()

    def perform_crossfade(self):
        current_volume = self.audio_output_current.volume()
        next_volume = self.audio_output_next.volume()

        if current_volume > 0:
            new_current_volume = max(0, current_volume - self.fade_step)
            self.audio_output_current.setVolume(new_current_volume)

        if next_volume < 1.0:
            new_next_volume = min(1.0, next_volume + self.fade_step)
            self.audio_output_next.setVolume(new_next_volume)

        if (
            self.audio_output_current.volume() == 0
            and self.audio_output_next.volume() == 1.0
        ):
            self.crossfade_timer.stop()
            self.player_current.stop()
            end_timestamp = self.get_current_timestamp()
            current_song = self.mp3_files[self.current_song_index]
            print(f"[INFO] Finished playing: {current_song} at {end_timestamp}")
            # Swap players without disconnecting signals
            self.player_current, self.player_next = (
                self.player_next,
                self.player_current,
            )
            self.audio_output_current = self.audio_output_next
            self.audio_output_next = self.audio_output_current
            self.fading = False
            print("[INFO] Crossfade completed and players swapped.")

    def on_media_status_changed(self, status):
        sender = self.sender()
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            end_timestamp = self.get_current_timestamp()
            if sender == self.player_current and not self.fading:
                current_song = self.mp3_files[self.current_song_index]
                print(f"[INFO] Finished playing: {current_song} at {end_timestamp}")
                self.current_song_index = (self.current_song_index + 1) % len(
                    self.mp3_files
                )
                self.play_current_song()
            elif sender == self.player_next:
                next_song = self.mp3_files[self.next_song_index]
                print(f"[INFO] Finished playing: {next_song} at {end_timestamp}")
                # No additional action needed as crossfade handles the transition

    def emit_done_signal(self):
        if self.status == 1:
            self.is_done_signal.emit(self.index)
            print(
                f"[INFO] Emit done signal for index {self.index} at "
                f"{self.get_current_timestamp()}"
            )
        self.status = 2

    def open_help_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Help")  # Optional: Set window title

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
            print(f"[INFO] Help accepted at {self.get_current_timestamp()}")
        else:
            print(f"[INFO] Help canceled at {self.get_current_timestamp()}")
        dialog.close()

    def get_current_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def on_player_metadata_changed(self, player):
        print("[DEBUG] Metadata changed for player:", player)
        meta = player.metaData()

        if meta.isEmpty():
            print("[DEBUG] No metadata available.")
            return

        print("[INFO] Current Song Metadata:")
        for key in meta.keys():  # noqa: SIM118 This is the only way to get the keys
            key_name = QMediaMetaData.metaDataKeyToString(key)

            try:
                value = meta.value(key)
            except RuntimeError as err:
                # This handles the "Can't find converter for
                # 'QMediaFormat::FileFormat'" error
                print(f"   {key_name}: [Unconvertible type: {err}]")
                continue

            print(f"   {key_name}: {value}")
