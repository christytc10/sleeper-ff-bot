import requests
from bot_interface import BotInterface


class Discord(BotInterface):
    def __init__(self, webhook):
        self.webhook = webhook

    def __init__(self, webhook, username, avatar_url):
        self.webhook = webhook
        self.username = username
        self.avatar_url = avatar_url

    def send_message(self, message):
        if self.username is None:
            requests.post(self.webhook, json={"content": message})
        else:
            requests.post(self.webhook, json={"username": self.username, "avatar_url": self.avatar_url, "content": message})

