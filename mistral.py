import os

from mistralai.client import MistralClient


MISTRAL_TOKEN = os.getenv("MISTRAL_TOKEN")
client = MistralClient(api_key=MISTRAL_TOKEN)

def run_mistral(user_message, context, model="mistral-large-latest"):
    chat_response = client.chat(
        model=model,
        messages=context
    )
    return chat_response.choices[0].message.content


if __name__ == "__main__":
    result = run_mistral("what is your name?")
    print(result)
