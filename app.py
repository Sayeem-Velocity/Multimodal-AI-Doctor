# gradio_app.py
from dotenv import load_dotenv
load_dotenv()

import os
import gradio as gr

from doctor_brain import encode_image, analyze_image_with_query
from patient_voice import transcribe_with_groq
from doctor_voice import text_to_speech_with_elevenlabs, text_to_speech_with_gtts


# ---------- Styling (CSS) ----------
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

:root {
  --bg: #0b1220;
  --grad1: #0b1220;
  --grad2: #101c3a;
  --grad3: #1e2a55;
  --card: rgba(255,255,255,0.06);
  --card-brd: rgba(255,255,255,0.14);
  --accent: #7aa2ff;
  --accent-2: #9b87f5;
  --accent-3: #3be4ff;
  --text: #e9eefc;
  --muted: #b8c2e0;
  --success: #22d3a3;
}

* { font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; }

body, .gradio-container, #root, .app {
  min-height: 100vh;
  background:
    radial-gradient(1200px 700px at 10% -10%, var(--grad3), transparent 40%),
    radial-gradient(1000px 700px at 110% 10%, var(--grad2), transparent 35%),
    linear-gradient(180deg, var(--grad1), #0a0f1c 70%);
  color: var(--text);
  overflow-x: hidden;
  position: relative;
}

/* ----- Floating Orbs (pure CSS) ----- */
.bg-orb, .bg-orb-2, .bg-orb-3 {
  position: fixed;
  pointer-events: none;
  z-index: 0;
  filter: blur(32px);
  opacity: 0.35;
  mix-blend-mode: screen;
  will-change: transform;
}
.bg-orb {
  width: 520px; height: 520px; top: 8%; left: -120px;
  background: radial-gradient(circle at 30% 30%, var(--accent-2), transparent 60%);
  animation: float1 14s ease-in-out infinite;
}
.bg-orb-2 {
  width: 420px; height: 420px; bottom: 6%; right: -100px;
  background: radial-gradient(circle at 70% 70%, var(--accent), transparent 60%);
  animation: float2 18s ease-in-out infinite;
}
.bg-orb-3 {
  width: 360px; height: 360px; top: 50%; left: 60%;
  background: radial-gradient(circle at 50% 50%, var(--accent-3), transparent 60%);
  animation: float3 16s ease-in-out infinite;
}
@keyframes float1 { 0%,100%{ transform: translateY(-10px)} 50%{ transform: translateY(18px)} }
@keyframes float2 { 0%,100%{ transform: translateY(12px)} 50%{ transform: translateY(-16px)} }
@keyframes float3 { 0%,100%{ transform: translateX(-10px)} 50%{ transform: translateX(16px)} }

/* ----- Header Title ----- */
#app-title {
  position: relative;
  font-weight: 800;
  letter-spacing: 0.2px;
  background: linear-gradient(90deg, var(--accent), var(--accent-2), var(--accent-3));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-size: 2.6rem;
  margin: 6px 0 6px 0;
  text-shadow: 0 8px 24px rgba(123,162,255,0.15);
  animation: glowPulse 3.6s ease-in-out infinite;
}
@keyframes glowPulse {
  0%,100% { filter: drop-shadow(0 0 0px rgba(123,162,255,0.35)); }
  50%     { filter: drop-shadow(0 0 14px rgba(123,162,255,0.55)); }
}
#app-title:after {
  content: "";
  display: block;
  width: 150px; height: 3px; margin: 10px auto 0;
  background: linear-gradient(90deg, transparent, var(--accent-2), transparent);
  border-radius: 3px;
  animation: shimmer 2.8s linear infinite;
}
@keyframes shimmer {
  0% { transform: translateX(-30px); opacity: 0.4; }
  50% { transform: translateX(30px); opacity: 1; }
  100% { transform: translateX(-30px); opacity: 0.4; }
}

#app-subtitle {
  color: var(--muted);
  font-weight: 400;
  font-size: 1rem;
  margin-bottom: 18px;
}

/* ----- Glass Cards ----- */
.glass {
  position: relative;
  background: var(--card);
  border: 1px solid var(--card-brd);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 18px;
  box-shadow:
    0 10px 30px rgba(0,0,0,0.20),
    inset 0 1px 0 rgba(255,255,255,0.04);
  transition: transform 240ms ease, box-shadow 240ms ease, border-color 240ms ease;
  z-index: 1;
}
.glass:hover {
  transform: translateY(-4px);
  border-color: rgba(155,135,245,0.55);
  box-shadow:
    0 16px 42px rgba(0,0,0,0.35),
    0 0 32px rgba(155,135,245,0.25);
}

.section-title {
  font-weight: 700;
  letter-spacing: 0.2px;
  margin-bottom: 8px;
  color: var(--text);
}

.hint {
  color: var(--muted);
  font-size: 0.9rem;
  margin-top: -4px;
  margin-bottom: 12px;
}

/* ----- Buttons (Magnetic + Shine) ----- */
.gradio-container .btn-primary, .gr-button.primary {
  position: relative;
  background: linear-gradient(135deg, var(--accent), var(--accent-2)) !important;
  border: none !important;
  color: white !important;
  box-shadow: 0 10px 26px rgba(123, 162, 255, 0.38);
  transform: translateZ(0);
  transition: transform 180ms ease, box-shadow 180ms ease, filter 180ms ease;
  overflow: hidden;
  border-radius: 12px !important;
}
.gradio-container .btn-primary:hover, .gr-button.primary:hover {
  filter: brightness(1.05);
  transform: translateY(-2px) scale(1.01);
  box-shadow: 0 16px 34px rgba(123, 162, 255, 0.45);
}
.gradio-container .btn-primary::after, .gr-button.primary::after {
  content: "";
  position: absolute;
  top: -100%; left: -30%;
  width: 60%; height: 300%;
  transform: rotate(25deg);
  background: linear-gradient( to right, rgba(255,255,255,0.0), rgba(255,255,255,0.35), rgba(255,255,255,0.0) );
  transition: left 500ms ease;
}
.gradio-container .btn-primary:hover::after, .gr-button.primary:hover::after {
  left: 110%;
}

/* Secondary buttons, if any */
button, .gr-button {
  border-radius: 12px !important;
}

/* Inputs focus */
textarea, input, .gr-textbox, .gr-text, .gradio-container .input-text, .gradio-container .wrap input[type="file"] {
  color: var(--text) !important;
}
.gradio-container .wrap input:focus, .gr-textbox:focus, textarea:focus {
  outline: none !important;
  box-shadow: 0 0 0 3px rgba(123,162,255,0.35) !important;
  border-color: rgba(123,162,255,0.6) !important;
}

/* Component labels */
label, .wrap .label, .label-wrap .label, .component .label {
  color: var(--muted) !important;
}

/* Layout */
.card-pad { padding: 18px; }
.grid {
  display: grid;
  gap: 16px;
  grid-template-columns: 1fr;
}
@media (min-width: 980px) {
  .grid { grid-template-columns: 1fr 1fr; }
}

.footer-note {
  color: var(--muted);
  text-align: center;
  font-size: 0.85rem;
  margin-top: 12px;
}

/* ----- Floating Badge ----- */
.fab {
  position: fixed;
  right: 20px; bottom: 20px;
  z-index: 3;
}
.fab .pill {
  display: inline-flex; align-items: center; gap: 10px;
  padding: 10px 14px;
  border-radius: 999px;
  background: linear-gradient(135deg, rgba(123,162,255,0.18), rgba(155,135,245,0.18));
  border: 1px solid rgba(255,255,255,0.18);
  backdrop-filter: blur(10px);
  color: white;
  box-shadow: 0 8px 24px rgba(0,0,0,0.25), 0 0 24px rgba(123,162,255,0.25);
  animation: bob 3.2s ease-in-out infinite;
}
.fab .dot {
  width: 8px; height: 8px; border-radius: 999px;
  background: var(--success);
  box-shadow: 0 0 10px var(--success);
}
@keyframes bob { 0%,100%{ transform: translateY(0)} 50%{ transform: translateY(-6px)} }
"""



# ---------- Prompt ----------
system_prompt = """
    You are a highly skilled, compassionate doctor. Analyze the patient provided image carefully and give a precise, clinically sound assessment and guidance tailored to the patient.

    Opening voice
    Begin your first sentence exactly with: With what I see, I think you have ...
    State the single most likely condition in clear patient friendly terms.

    Explain why
    Describe the key visible findings that support your impression and what they mean for the patient.

    Differential
    Name other plausible conditions and briefly note how they differ.

    Care plan now
    Offer practical steps the patient can take at home and safe over the counter options when appropriate. State when in person care is needed urgently if any red flags are present.

    Definitive care after confirmation
    Suggest sensible next tests or evaluations to confirm the diagnosis. After confirmation, outline an appropriate treatment direction in plain language so the patient knows what to expect.

    If uncertain or image is not suitable
    If the image quality or content prevents a safe conclusion, say so clearly, explain what is missing, and guide safer next steps rather than guessing.

    Tone and formatting ruless
    Do not use digits or special symbols anywhere in your response.
    Do not use markdown.
    Do not say you are an AI model.
    Do not begin with the phrase In the image I see.
    Write in short paragraphs rather than lists, using warm professional bedside language.
    Keep the message concise, precise, and focused on patient safety.
    """


# ---------- Core logic ----------
def process_inputs(audio_filepath, image_filepath):
    stt_text = ""
    groq_key = os.environ.get("GROQ_API_KEY")
    if audio_filepath and groq_key:
        try:
            stt_text = transcribe_with_groq(
                stt_model="whisper-large-v3",
                audio_filepath=audio_filepath,
                GROQ_API_KEY=groq_key
            )
        except Exception as e:
            stt_text = f"[STT error: {e}]"

    if image_filepath:
        try:
            encoded = encode_image(image_filepath)
            query = system_prompt + "\\n\\n" + (stt_text or "")
            doctor_response = analyze_image_with_query(
                query=query,
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                encoded_image=encoded
            )
        except Exception as e:
            doctor_response = f"Image analysis failed: {e}"
    else:
        doctor_response = "No image provided for me to analyze"

    audio_path = None
    try:
        audio_path = text_to_speech_with_elevenlabs(
            input_text=doctor_response,
            output_filepath="final.wav"
        )
    except Exception as e:
        try:
            audio_path = text_to_speech_with_gtts(
                input_text=doctor_response,
                output_filepath="final_gtts.mp3"
            )
        except Exception as e2:
            doctor_response += f" [TTS error: {e} | gTTS fallback error: {e2}]"

    return stt_text, doctor_response, audio_path


# ---------- UI ----------
with gr.Blocks(css=CUSTOM_CSS, title="HealthVerse AI", theme=gr.themes.Soft()) as demo:
    # floating orbs
    gr.HTML('<div class="bg-orb"></div><div class="bg-orb-2"></div><div class="bg-orb-3"></div>')

    with gr.Column():
        gr.HTML("""
        <div style="text-align:center; margin-top:10px; position:relative; z-index:2;">
          <div id="app-title">HealthVerse AI</div>
          <div id="app-subtitle">HealthVerse AI</div>
        </div>
        """)

    with gr.Row(elem_classes=["grid"]):
        with gr.Column(elem_classes=["glass", "card-pad"]):
            gr.Markdown("### Inputs", elem_classes=["section-title"])
            gr.Markdown("Upload an image and Tell about your symptoms.", elem_classes=["hint"])
            audio_in = gr.Audio(sources=["microphone"], type="filepath", label="Patient's Voice (optional)")
            image_in = gr.Image(type="filepath", label="Image for diagnosis")
            submit_btn = gr.Button("Analyze", variant="primary")
        with gr.Column(elem_classes=["glass", "card-pad"]):
            gr.Markdown("### Results", elem_classes=["section-title"])
            stt_out = gr.Textbox(label="Speech to Text", interactive=False, lines=3)
            doc_out = gr.Textbox(label="Doctor's Response", interactive=False, lines=5)
            audio_out = gr.Audio(label="Doctor's Voice", type="filepath")

    gr.HTML('<div class="footer-note">Made By S.M. Shahriar &amp; Adiba Sabreen</div>')

    # floating badge
    gr.HTML("""
    <div class="fab">
      <div class="pill">
        <span class="dot"></span>
        <strong>HealthVerse AIr</strong>
        <span style="opacity:.8;">is listening</span>
      </div>
    </div>
    """)

    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_in, image_in],
        outputs=[stt_out, doc_out, audio_out]
    )

if __name__ == "__main__":
    demo.queue().launch(debug=True)
