import telebot
import json


class Telegram:
    def __init__(self):
        with open('api_telegram.json') as json_file:
            data = json.load(json_file)

            self.token = data['token']
            self.ch_id = data['ch_id']
            self.tb = telebot.TeleBot(self.token)

    def enviar_mensajes_a_telegram(self, url):
        self.tb.send_message(self.ch_id, url)

