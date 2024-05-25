import gradio as gr

from rags import rag_question

class CurrentUser:
    name = "undefined"
    is_doctor = False
    menu_added = False

def bot(message, history):
    return rag_question("oleg", message)


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


DOCTORS = {
    "victoria",
}

USERS = {
    "oleg", "nick"
}

def test(request: gr.Request):
    return "Welcome, " + request.username


def do_auth(username, password):
    CurrentUser.name = username
    if username in DOCTORS:
        CurrentUser.is_doctor = True
        if not CurrentUser.menu_added:
            t = gr.Textbox()
            gradio_app.load(test, None, t)
            gradio_app.add(gr.Dropdown(list(USERS)))

        return True
    if username in USERS:
        CurrentUser.is_doctor = False
        return True

    return False


if __name__ == "__main__":
    gradio_app.launch(auth=do_auth)
