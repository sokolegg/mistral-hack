import gradio as gr

from rags import rag_question, prepare_data
from app import USERS

DOCTORS = {
    "victoria", "johnson", "admin"
}


class CurrentUser:
    name = "undefined"
    is_doctor = False
    menu_added = False

class UploadUser:
    name = "undefined"

def bot(message, history):
    return rag_question(CurrentUser.name, message)


def test(request: gr.Request):
    return gr.UploadButton("Add more medical files " + request.username)


def do_auth(username, password):
    CurrentUser.name = username
    if username in DOCTORS:
        CurrentUser.is_doctor = False
        return True

    return False

def upload_file(file):
    print(type(file))
    if isinstance(file, str):
        bts = open(file, "rb").read()
    import random
    with open(f"data/{UploadUser.name}/{random.randint(1, 2**32)}.txt", "wb") as f:
        f.write(bts)
        prepare_data()
    print(f"upload file")


def change_upload_user(username):
    UploadUser.name = username


with gr.ChatInterface(
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
    additional_inputs=[

    ]
) as gradio_app:
    d = gr.Dropdown(list(USERS))
    u = gr.UploadButton("Upload medical document", file_count="single")
    u.upload(upload_file, u, )
    d.change(change_upload_user, d, )



if __name__ == "__main__":
    gradio_app.launch(auth=do_auth, server_port=7789)
