import requests
from config import token_telegram, chat_id


def send_telegram(text: str):
    url = "https://api.telegram.org/bot"
    url += token_telegram
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": chat_id,
        "text": text
    })

    if r.status_code != 200:
        raise Exception("post_text error")
