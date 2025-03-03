import pyttsx3
from loguru import logger

from slumber import settings

MIN_VOLUME = 0
MAX_VOLUME = 100

# TODO: make a wrapper class for this


def init_text2speech_engine(
    rate: int = settings["text2speech"]["rate"],
    volume: int = settings["text2speech"]["volume"],
    voice: str | None = None,
) -> pyttsx3.Engine:
    """
    Initialize a text-to-speech engine with the given rate, volume, and voice.
    Args:
        rate (int, optional): Speaking rate in words per minute.
        volume (float, optional): Volume level between 0.0 and 1.0.
        voice (str, optional): Voice identifier.
    Returns:
        pyttsx3.Engine: Initialized TTS engine.
    """

    if rate <= 0:
        raise ValueError("Rate must be greater than 0.")

    if volume < MIN_VOLUME or volume > MAX_VOLUME:
        raise ValueError(f"Volume must be between {MIN_VOLUME} and {MAX_VOLUME}.")

    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume / MAX_VOLUME)

    if voice is not None:
        voices = engine.getProperty("voices")
        voice_ids = [voice.id for voice in voices]

        if voice not in voice_ids:
            raise ValueError(
                f"Voice '{voice}' not found. Available voices: {voice_ids}"
            )

        engine.setProperty("voice", voice)

    voice = engine.getProperty("voice")

    logger.info(
        f"Initialized TTS engine with rate: {rate}, volume: {volume}, voice: {voice}"
    )
    return engine


def text2speech(text: str, engine: pyttsx3.Engine | None = None) -> None:
    """
    Convert text to speech. If no engine is provided,
    it constructs a new TTS engine instance or reuses the existing instance.

    Args:
        text (str): Text to convert to speech
        engine (pyttsx3.Engine, optional): TTS engine instance.

    Example:
        ```python
        # Set up custom engine
        engine = init_text2speech_engine(
            rate=150, volume=0.8, voice="com.apple.voice.compact.en-US.Samantha"
        )

        # Pass the configured engine
        text2speech("Hello, this is a test message", engine=engine)
        ```
    """
    logger.debug(f"Text to speech: {text}")
    engine = engine or init_text2speech_engine()
    engine.say(text)
    engine.runAndWait()


def try_voices(
    engine: pyttsx3.Engine | None = None,
    text: str = "The quick brown fox jumps over the lazy dog.",
) -> None:
    """
    Try out all available voices and print their details.
    """
    engine = engine or init_text2speech_engine()
    voices = engine.getProperty("voices")
    logger.info(f"Available voices: {len(voices)}")
    for voice in voices:
        logger.info(
            f"Voice ID: {voice.id}, Name: {voice.name},"
            f" Languages: {voice.languages}, Gender: {voice.gender}"
        )
        engine.setProperty("voice", voice.id)
        engine.say(text)
        engine.runAndWait()
