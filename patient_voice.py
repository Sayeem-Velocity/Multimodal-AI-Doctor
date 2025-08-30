from dotenv import load_dotenv
load_dotenv()

import logging
from io import BytesIO
import os
import speech_recognition as sr
from pydub import AudioSegment
from groq import Groq

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def record_audio(file_path: str, timeout: int = 20, phrase_time_limit: int | None = None) -> str:
    """
    Record audio from microphone and save as MP3 (requires ffmpeg on PATH).
    Returns saved file path.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            wav_bytes = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_bytes))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            logging.info(f"Audio saved to {file_path}")
            return file_path
    except Exception as e:
        logging.error(f"Recording error: {e}")
        raise

def transcribe_with_groq(stt_model: str, audio_filepath: str, GROQ_API_KEY: str) -> str:
    """
    Transcribe audio using Groq Whisper.
    """
    client = Groq(api_key=GROQ_API_KEY)
    with open(audio_filepath, "rb") as f:
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=f,
            language="en"
        )
    return transcription.text


