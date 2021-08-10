import requests
import json

with open('config.json') as config_file:
    data = json.load(config_file)
    token = data["token"]
    chatID = data["chatID"]


def send_telegram(text: str):
    url = "https://api.telegram.org/bot"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": chatID,
        "text": text
    })

    if r.status_code != 200:
        raise Exception("post_text error")
