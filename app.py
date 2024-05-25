import gradio as gr

from rags import rag_question

def bot(message, history):
    return rag_question("oleg", message)


gradio_app = gr.ChatInterface(
    bot,
    chatbot=gr.Chatbot(height=600),
    textbox=gr.Textbox(placeholder="Ask me a medical question ", container=False, scale=7),
    title="Project Alice 👩‍⚕️",
    description="Ask me any health question",
    theme="soft",
    examples=["What tablets do I need to drink?", "Can I drink alcohol?", ],
    cache_examples=True,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
    additional_inputs=[
        gr.Textbox("You are helpful AI.", label="System Prompt"),
        gr.File()
    ],
)

if __name__ == "__main__":
    gradio_app.launch()
