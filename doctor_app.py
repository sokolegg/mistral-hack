import gradio as gr

from rags import rag_question


DOCTORS = {
    "victoria",
}

USERS = {
    "oleg", "nick", "leon"
}


class CurrentUser:
    name = "undefined"
    is_doctor = False
    menu_added = False

def bot(message, history):
    return rag_question("oleg", message)


def test(request: gr.Request):
    return gr.UploadButton("Add more medical files " + request.username)


def do_auth(username, password):
    CurrentUser.name = username
    if username in DOCTORS:
        CurrentUser.is_doctor = True
        return True
    if username in USERS:
        CurrentUser.is_doctor = False
        return True

    return False

gradio_app = gr.ChatInterface(
    bot,
    chatbot=gr.Chatbot(height=600),
    textbox=gr.Textbox(placeholder="Ask me any medical question", container=False, scale=7),
    title="Project Alice 👩‍⚕️",
    description="Ask me any health question",
    theme="soft",
    examples=["What tablets do I need to drink?", "Can I drink alcohol?", ],
    cache_examples=True,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
)


if __name__ == "__main__":
    gradio_app.launch(auth=do_auth)
