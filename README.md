# Wallapop crawler

Crawler creado mediante la librería Selenium de python. Se ha añadido la funcionalidad de que cada anuncio que se visita se envía la URL del producto a tu grupo propio de Telegram (Mirar en configuración de Telegram)

# Instalacion
`$ git clone https://github.com/KevinLiebergen/wallapop_crawler.git`
<br>`$ cd wallapop_crawler`
<br>`$ pip3 install virtualenv`
<br>`$ virtualenv venv`

Instalación Firefox driver, 2 opciones:

- Mediante script instalación
<br>`$ sh gecko_installation.sh`

- A mano paso por paso
```
$ wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
$ tar xvfz geckodriver-v0.24.0-linux64.tar.gz
$ sudo mv geckodriver /usr/local/bin
$ rm geckodriver-v0.24.0-linux64.tar.gz
```
# Descarga librerías
```
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```

# Ejecución
`(venv) $ python3 crawler_walla.py`

# Configuración Telegram

Este script implementa la opción de enviar los anuncios a un grupo privado de Telegram, para ello es necesario:
- Crear tu propio bot
    - Comienza una conversación con `@BotFather` y escribe `/newbot`. Especifica el nombre y el nickname
- Crear un grupo y añadir el bot creado
- Conocer el __token__ del bot creado (Botfather al crear tu bot te lo escribe por pantalla) y __dale valor a la variable token con el token de tu bot__ en el método `configurar_telegram()`
- Conocer el __chat id__ del grupo creado y darle valor a la variable __ch_id__ del método `configurar_telegram()`

<br>[Video resumen como crear tu bot y conocer tu token y chat id](https://www.youtube.com/watch?v=UhZtrhV7t3U)

<br>Para deshabilitar esta opción únicamente es necesario comentar las llamadas a los métodos `configurar_telegram()
` y `enviar_mensajes_a_telegram(producto["url"])` cerca de las líneas 182 y 158 respectivamente.

# Salida entorno virtual

`(venv) $ deactivate`

