# frontend/app.py
import gradio as gr
import requests
import os

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000")
CHAT_ENDPOINT = f"{BACKEND_URL}/chat"

def send_to_backend(message: str):
    """Send message to FastAPI backend /chat. Returns reply text."""
    try:
        r = requests.post(CHAT_ENDPOINT, json={"message": message}, timeout=15)
        r.raise_for_status()
        data = r.json()
        return data.get("reply", "No reply from backend.")
    except Exception as e:
        return f"Error contacting backend: {e}"

def chat_fn(user_message, history):
    # `history` now uses OpenAI message dicts format with 'role' and 'content'
    backend_reply = send_to_backend(user_message)
    history = history or []
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": backend_reply})
    return "", history

with gr.Blocks(title="Trip Curator — Chat UI (Gradio)") as demo:
    gr.Markdown("# 🌍 Trip Curator\nAsk about trips and get curated itineraries.")

    chatbot = gr.Chatbot(type="messages", label="Trip Assistant Chat")
    txt = gr.Textbox(
        show_label=False,
        placeholder="Ask me about your trip and press Enter",
        container=False,
    )

    txt.submit(chat_fn, [txt, chatbot], [txt, chatbot])
    clear_btn = gr.Button("Clear Chat")
    clear_btn.click(lambda: [], None, chatbot)  # simply returns empty list to reset

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)), share=False)

