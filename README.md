# Wallapop crawler

Crawler creado mediante la librería Selenium de python. Se han implementado funcionalidades para:
- Que cada anuncio que se visita se envía la URL del producto a tu grupo propio de Telegram (Mirar en configuración de Telegram).
- Anuncios crawleados se guardan en un csv.
- Se muestra por terminal los productos.
- Los productos se guarden a una base de datos con sus respectivos campos.

# Instalacion

```shell
$ git clone https://github.com/KevinLiebergen/wallapop_crawler.git
$ cd wallapop_crawler
$ pip3 install virtualenv
$ virtualenv venv
```

Setup entorno:

- Mediante script instalación
```shell
$ cd setup
$ sh setup.sh
````

* Credenciales MySQL
  * Usuario: 'walla_user' 
  * Contraseña: 'walla_password'

- Instalación Gecko driver paso por paso

```shell
$ wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
$ tar xvfz geckodriver-v0.24.0-linux64.tar.gz
$ sudo mv geckodriver /usr/local/bin
$ rm geckodriver-v0.24.0-linux64.tar.gz
```
# Descarga librerías

```shell
$ source venv/bin/activate

(venv) $ pip3 install -r requirements.txt
```

# Ejecución

Únicamente ejecutar el script, por defecto viene configurado, antes de ejecutarlo leer detenidamente la sección de __configuración Telegram__ y __conexión base de datos__ para saber si comentar o no esa parte del código. 
<br> `(venv) $ cd project`
<br>`(venv) $ python3 main.py`

Para ejecutar desde Docker (En desarrollo, hay fallos):

- Para configurar el envío de mensajes a Telegram lee detenidamente la sección __configuración Telegram__, si no deseas el envío de mensajes comenta las llamadas a los métodos `configurarTelegram()` y `enviar_mensajes_a_telegram()`.
- Activa la opción `options.headless = True` en la línea 274 
- Construye y ejecuta la siguiente imagen en modo interactivo:
```bash
$ docker build . -t walla_crawler
$ docker run -it walla_crawler
```

Para docker-compose (Falta mucho aun no funciona)

__TAREA HACER CUANDO VUELVA VIAJE__
leer https://robertoorayen.eu/2017/05/14/como-crear-un-sitio-web-con-docker/ para entender el puenteo entre puertos
no va bien por los puertos, entender como crawler a la imagen mysql y este a maquina local

```bash
$ docker-compose build
$ docker-compose run crawler
```
__No se puede hacer `$ docker-compose up` porque up no es interactivo, por eso hacemos run crawler__

# Configuración Telegram

Este script implementa la opción de enviar los anuncios a un grupo privado de Telegram, para ello es necesario:
- Crear tu propio bot
    - Comienza una conversación con `@BotFather` y escribe `/newbot`. Especifica el nombre y el nickname
- Crear un grupo y añadir el bot creado
- Conocer el __token__ del bot creado (Botfather al crear tu bot te lo escribe por pantalla) y __dale valor a la variable token con el token de tu bot__ en el fichero api_telegram.json.
- Conocer el __chat id__ del grupo creado y darle valor a la variable __ch_id__ en el fichero api_telegram.json.

<br>[Video resumen como crear tu bot y conocer tu token y chat id](https://www.youtube.com/watch?v=UhZtrhV7t3U)

<br>Para deshabilitar esta opción únicamente es necesario comentar las llamadas a los métodos 
`configurar_telegram()` y `enviar_mensajes_a_telegram(producto["url"])` __cerca__ del fichero `crawler.py` y la instanciación, 
`telegram.Telegram()` del mismo fichero.

# Conexión base de datos

Se ha implementado una opción para conectar los productos crawleados a una base de datos.

### Instalación base de datos mysql

```bash
$ sudo apt update
$ sudo apt install mysql-server
$ sudo mysql_secure_installation
```

### Configuración base de datos

Configuro una contraseña para acceder a la base de datos, creo la base de datos `crawler`.

`$ sudo mysql`
```mysql
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
mysql> CREATE DATABASE crawler;
mysql> exit
```

Una vez esté instalado, al ejecutar el script se creará la respectiva tabla de la base de datos y se guardarán las consultas en dicha base de datos. Si se quiere omitir comentar las llamadas a los métodos `guardar_elemento_bbdd(producto)` y `cursor, db = configurar_bbdd()` en las líneas 182 y 261 respectivamente.

Si se desea acceder a la base de datos se accederá con:
<br>`$ mysql -u root -p`
<br>La contraseña solicitada será __root__

# Salida entorno virtual

`(venv) $ deactivate`

