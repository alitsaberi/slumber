import winsound
from contextlib import contextmanager
from pathlib import Path

from comtypes import CLSCTX_ALL
from loguru import logger
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

MIN_VOLUME = 0
MAX_VOLUME = 100


def get_system_volume() -> int:
    volume = _get_audio_interface()
    return int(volume.GetMasterVolumeLevelScalar() * MAX_VOLUME)


def set_system_volume(volume_level: int) -> None:
    if volume_level < MIN_VOLUME or volume_level > MAX_VOLUME:
        raise ValueError(f"Volume level must be between {MIN_VOLUME} and {MAX_VOLUME}.")

    volume = _get_audio_interface()
    # Set volume level (0.0 to 1.0)
    volume.SetMasterVolumeLevelScalar(volume_level / MAX_VOLUME, None)


def _get_audio_interface() -> IAudioEndpointVolume:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return interface.QueryInterface(IAudioEndpointVolume)


def play_sound(sound_path: Path) -> None:
    winsound.PlaySound(str(sound_path), winsound.SND_FILENAME)


@contextmanager
def temporary_volume(target_volume: int):
    previous_volume = get_system_volume()
    logger.debug(f"Setting system volume to {target_volume} from {previous_volume}")
    set_system_volume(target_volume)
    try:
        yield
    finally:
        logger.debug(f"Setting system volume to {previous_volume} from {target_volume}")
        set_system_volume(previous_volume)
