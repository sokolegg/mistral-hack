import gradio as gr
import weave

from rags import rag_question
from mistralai.models.chat_completion import ChatMessage

USERS = {
    "nick", "leon"
}


class CurrentUser:
    name = "undefined"
    is_doctor = False
    menu_added = False

def bot(message, history):
    history_for_mistral = []
    for human, assistant in history:
        history_for_mistral.append(ChatMessage(role="user", content=human))
        history_for_mistral.append(ChatMessage(role="assistant", content=assistant))
    history_for_mistral.append(ChatMessage(role="user", content=message))

    return rag_question(CurrentUser.name, history_for_mistral)


def do_auth(username, password):
    CurrentUser.name = username
    if username in USERS:
        CurrentUser.is_doctor = False
        return True

    return False

gradio_app = gr.ChatInterface(
    bot,
    chatbot=gr.Chatbot(height=400),
    textbox=gr.Textbox(placeholder="Ask me any medical question", container=False, scale=7),
    title="Project Alice 👩‍⚕️",
    description="Ask me any health question",
    theme="soft",
    examples=["What tablets do I need to drink?", "Can I drink alcohol?", ],
    cache_examples=False,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
)


if __name__ == "__main__":
    gradio_app.launch(auth=do_auth)
