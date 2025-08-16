import os
import gradio as gr
from groq import Groq

# ====== API Key Handling ======

os.environ["GROQ_API_KEY"] = "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"
api_key = os.environ.get("GROQ_API_KEY", "").strip()
if not api_key:
    raise ValueError("⚠️ GROQ_API_KEY is not set. Please add it in your Space settings.")

# ====== Model Config ======
GROQ_MODEL = "llama-3.3-70b-versatile"

# ====== System Prompt ======
SYSTEM_PROMPT = (
    "You are a professional AI writing assistant. "
    "Generate high-quality content based on the user's inputs. "
    "Follow the requested tone, format, and language. "
    "Output ONLY the final content—no explanations."
)

# ====== AI Content Generation Function ======
def generate_content(topic, tone, audience, length, language):
    if not topic.strip():
        return "Please enter a topic for the content."
    try:
        client = Groq(api_key=api_key)
        user_prompt = (
            f"Topic: {topic}\n"
            f"Tone: {tone}\n"
            f"Audience: {audience}\n"
            f"Length: {length}\n"
            f"Language: {language}"
        )
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error: {e}"

# ====== Gradio UI ======
with gr.Blocks(title="📝 AI Writing Assistant / Copy Generator") as demo:
    gr.HTML(
        """
        <div style='text-align:center; padding:20px; background-color:#1E293B; border-radius:12px;'>
            <h1 style='color:#38BDF8;'>📝 LingoAI Writing Assistant</h1>
            <p style='color:white; font-size:1.2em;'>Generate high-quality blog posts, ads, emails, or social media content instantly!</p>
        </div>
        """
    )

    with gr.Row():
        with gr.Column(scale=3):
            topic_input = gr.Textbox(label="📌 Topic", placeholder="Enter your topic here...", lines=2)
            tone_input = gr.Textbox(label="🎯 Tone", placeholder="e.g., Formal, Casual, Persuasive", lines=1)
            audience_input = gr.Textbox(label="👥 Audience", placeholder="Describe your target audience", lines=1)
            length_input = gr.Textbox(label="⏳ Length / Word count", placeholder="e.g., 200 words", lines=1)
            language_input = gr.Textbox(label="🌐 Language", placeholder="e.g., English, Spanish", lines=1)
        with gr.Column(scale=1):
            generate_btn = gr.Button("🚀 Generate Content", variant="primary")
            output_box = gr.Textbox(label="📄 Generated Content", lines=15)

    generate_btn.click(
        generate_content,
        inputs=[topic_input, tone_input, audience_input, length_input, language_input],
        outputs=output_box
    )

    gr.HTML(
        """
        <div style='text-align:center; margin-top:20px; color:gray;'>
            <p>⚡ Powered by <b>Groq</b> & Llama 3 AI – Create content fast and effortlessly!</p>
        </div>
        """
    )

if __name__ == "__main__":
    demo.launch()
