from dotenv import load_dotenv
load_dotenv()

import os
import os.path as op

# gTTS library – produces MP3 audio (works fine in Gradio)
from gtts import gTTS

# ElevenLabs SDK
from elevenlabs.client import ElevenLabs
import elevenlabs


def text_to_speech_with_gtts(input_text: str, output_filepath: str) -> str:
    """
    Generate speech from text using Google's gTTS library.
    Produces MP3 output that can be played easily in Gradio.
    
    Args:
        input_text (str): Text to convert into speech
        output_filepath (str): Where to save the generated MP3 file
    
    Returns:
        str: Path to the saved MP3 file
    """
    gTTS(text=input_text, lang="en", slow=False).save(output_filepath)
    return output_filepath


def text_to_speech_with_elevenlabs(input_text: str, output_filepath: str) -> str:
    """
    Generate speech from text using ElevenLabs API.
    Produces WAV output (instead of MP3) to avoid issues with
    Windows SoundPlayer (which only supports WAV/PCM).
    
    Args:
        input_text (str): Text to convert into speech
        output_filepath (str): Desired output file path (extension adjusted to .wav)
    
    Returns:
        str: Path to the saved WAV file
    """
    # Fetch ElevenLabs API key from environment variables
    api_key = os.environ.get("ELEVEN_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVEN_API_KEY is not set in environment")

    # Replace whatever extension is provided with .wav
    base, _ = op.splitext(output_filepath)
    output_wav = base + ".wav"

    # Initialize ElevenLabs client
    client = ElevenLabs(api_key=api_key)

    # Generate audio with the ElevenLabs TTS model
    audio = client.generate(
        text=input_text,
        voice="Aria",          # Use a supported voice available in your account
        output_format="wav",   # WAV ensures compatibility across OS
        model="eleven_turbo_v2"
    )

    # Save audio to file
    elevenlabs.save(audio, output_wav)
    return output_wav
