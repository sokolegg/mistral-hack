import json
import os
import weave

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


MISTRAL_TOKEN = os.getenv("MISTRAL_TOKEN")
client = MistralClient(api_key=MISTRAL_TOKEN)

def run_mistral(context):
    print(f"context mistral: {context}")
    chat_response = client.chat(
        model="mistral-large-latest",
        messages=context
    )
    extracted = chat_response.choices[0].message.content
    print("testtttttttttttttttttttttttttttttttttttt")
    print(extracted)
    return extracted

@weave.op()
def run_mistral_one(message):
    print(f"context mistral: {message}")
    system_prompt = f"""\
You are Alice, a friendly medical doctor. You exist to chat with your patient Leon.
Be really concise and clear in your responses. You can use emojis to make the conversation more engaging.
Be informal in your responses, you are texting each other, be casual. Adapt to your patient's mood and tone.

Your patient is Leon and here is medical informations:
Leon is a 45 year old man, 183 cm, blue eyes and comes from Sokovia.
he has Alzeimher and a fragile intestins.
He also got a problem with alcohol.
He was addicted to morphine 3 years ago.

The Dr. Johnsonn write 15/05/2024 :
He likes to speak really friendly, like I am his best friend, he's always smiling and he's a good listener.
He speeks like in the street.
Acamprosate (Campral)	- Two pills taken three times a day
Disulfiram (Antabuse)	- One pill taken once a day
He often forget his second daughter, Rebecca, she's nine and always smiling, we call her "Hugging Face" because of that.
coffee Ristretto in the morning, keys in the second drawer and obviously put a pant before going out !

There is no other information about the patient, the data is correct and up to date.
Respond to the user last message not the whole conversation.

Current date: 26/05/2024 10:37 AM

Example of a good conversation:
Leon: Hi, should i take pills today?
Alice: Hi user ! It is 10:37 AM so yes you have to take your medication now. How are you feeling this morning? 😊 Did you sleep well ?
Leon: what pills should i take?
Alice: You should take your Acamprostate and Disulfiram pills 😊

Now it's your turn to respond to the user last message.
"""

    chat_response = client.chat(
        model="mistral-large-latest",
        messages=[ChatMessage(role="system", content=system_prompt), ChatMessage(role="user", content=message)]
    )
    extracted = chat_response.choices[0].message.content
    print("testtttttttttttttttttttttttttttttttttttt")
    print(extracted)
    return {"extracted": extracted}


weave.init("project-alice")
