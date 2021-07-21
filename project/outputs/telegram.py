import time

import telebot
import json
import os


def _saludar(file):
    print("[-] Leyendo fichero de configuración de Telegram en {} ".format(file))


class Telegram:
    def __init__(self):
        fichero_telegram = os.path.dirname(os.path.abspath(__file__)) + '/api_telegram.json'
        with open(fichero_telegram) as json_file:
            _saludar(json_file.name)
            data = json.load(json_file)

            self.token = data['token']
            self.ch_id = data['ch_id']
            self.tb = telebot.TeleBot(self.token)

    def enviar_mensajes_a_telegram(self, url, precio):

        time.sleep(1)
        seg_espera = 30

        for stop in range(10):
            try:
                self.tb.send_message(self.ch_id, "{} {}".format(precio, url))
                break
            except:
                print("[-] Demasiadas peticiones: esperando {} segundos".format(seg_espera))
                time.sleep(seg_espera)


