# Wallapop crawler

Crawler creado mediante la librería Selenium de python.

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
`(venv) $ python3 crawler.py`

# Salida entorno virtual

`(venv) $ deactivate`

