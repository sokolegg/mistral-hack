import os

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


MISTRAL_TOKEN = os.getenv("MISTRAL_TOKEN")
client = MistralClient(api_key=MISTRAL_TOKEN)

def run_mistral(user_message, model="mistral-medium-latest"):
    messages = [
        ChatMessage(role="user", content=user_message)
    ]
    chat_response = client.chat(
        model=model,
        messages=messages
    )
    return chat_response.choices[0].message.content


if __name__ == "__main__":
    result = run_mistral("what is your name?")
    print(result)
