from pathlib import Path

import pyttsx3
import yaml


def load_yaml(config_path: Path) -> dict:
    """Load a yaml file and return the contents as a dictionary.

    Args:
        config_path (Path): Path to the yaml file.

    Returns:
        dict: The contents of the yaml file.
    """
    with open(config_path) as file:
        config = yaml.safe_load(file)
    return config


def text2speech(text: str, engine: pyttsx3.Engine | None = None) -> None:
    """
    Convert text to speech. If no engine is provided,
    it constructs a new TTS engine instance or reuses the existing instance.

    Args:
        text (str): Text to convert to speech
        engine (pyttsx3.Engine | None): Optional TTS engine instance. Defaults to None.

    Example:
        ```python
        # Set up custom engine
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)  # Speaking rate in words per minute
        engine.setProperty("volume", 0.9)  # Volume between 0.0 and 1.0
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[0].id)  # Index 0 for first available voice

        # Pass the configured engine
        text2speech("Hello, this is a test message", engine=engine)
        ```
    """
    engine = engine or pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
