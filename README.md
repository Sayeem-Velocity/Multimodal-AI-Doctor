# AI Doctor

**AI Doctor** is a multimodal assistant built with **Gradio**, **Groq APIs**, and **ElevenLabs**.
It allows users to record patient voice, upload medical-related images, and receive a concise **doctor-style spoken response**.

---

## Features

* Record patient voice from microphone (Speech-to-Text using **Whisper Large v3** on Groq)
* Upload an image (diagnosis/medical-related) for analysis (Vision-Language reasoning using **Llama 4 Scout** on Groq)
* Generate a concise medical-style response (2 sentences maximum, human-like tone)
* Convert response to voice (Text-to-Speech using **ElevenLabs** with WAV output, fallback to **gTTS** if needed)
* Gradio-based interactive UI

---

## Project Structure

```
.
├── app.py                    # Gradio UI + main workflow
├── brain_of_the_doctor.py    # Image encoding + Groq multimodal analysis
├── voice_of_the_patient.py   # Audio recording + Groq Whisper transcription
├── voice_of_the_doctor.py    # ElevenLabs + gTTS text-to-speech
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (API keys)
├── .gitignore                # Ignore venv, __pycache__, .env, etc.
├── images/                   # Folder for saving test/sample images
└── README.md                 # Documentation
```

---

## Requirements

* Python 3.10 or higher
* FFmpeg installed and available in PATH (required by pydub)
* A Groq API key (obtain from [https://console.groq.com](https://console.groq.com))
* An ElevenLabs API key (obtain from [https://elevenlabs.io](https://elevenlabs.io))

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/ai-doctor-2.0-voice-and-vision.git
   cd ai-doctor-2.0-voice-and-vision
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install FFmpeg (if not already installed):

   * Windows: Download from [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/) and add `bin/` to PATH
   * Linux (Debian/Ubuntu): `sudo apt install ffmpeg`
   * macOS (Homebrew): `brew install ffmpeg`

5. Create a `.env` file in the project root with your API keys:

   ```
   GROQ_API_KEY=your_groq_api_key_here
   ELEVEN_API_KEY=your_elevenlabs_api_key_here
   ```

---

## Running the Application

Start the Gradio app:

```bash
python gradio_app.py
```

The app will launch locally at:

```
http://127.0.0.1:7860
```

---

## Usage

1. Allow microphone access to record your voice.
2. Upload a medical image for analysis.
3. The system will:

   * Transcribe your voice (Whisper Large v3 via Groq)
   * Analyze the image + text (Llama 4 Scout via Groq)
   * Generate a concise medical-style response
   * Play back the response as voice (ElevenLabs or gTTS fallback)

---

## Models Used

1. **Whisper Large v3** (Groq) – Speech-to-Text

   * [Groq API Docs](https://console.groq.com/docs)

2. **Llama 4 Scout 17B (Mixture-of-Experts)** (Groq) – Vision-Language reasoning

   * [Groq API Docs](https://console.groq.com/docs)

3. **ElevenLabs `eleven_turbo_v2`** – Text-to-Speech (WAV, with MP3 fallback)

   * [ElevenLabs Docs](https://elevenlabs.io/docs)

4. **gTTS (Google Text-to-Speech)** – Backup Text-to-Speech

   * [PyPI gTTS](https://pypi.org/project/gTTS/)

---

## Notes

* ElevenLabs free-tier accounts may not allow **WAV output** or certain custom voices. In that case, the code automatically falls back to **MP3** output with a safe built-in voice.
* Ensure FFmpeg is correctly installed; otherwise, audio export with pydub will fail.
* Gradio will automatically handle playback of both WAV and MP3 outputs.

---

## Support

For questions, issues, or collaboration, please contact:

**[sayeem26s@gmail.com](mailto:sayeem26s@gmail.com)**
**LinkedIn:** [https://www.linkedin.com/in/s-m-shahriar-26s/](https://www.linkedin.com/in/s-m-shahriar-26s/)

---
