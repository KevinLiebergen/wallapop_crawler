# Wallapop crawler

![](images_demo/principal.png )


Crawler creado mediante la librería Selenium de python. Se han implementado funcionalidades para:

- Que cada anuncio que se visita se envía la URL del producto a tu grupo propio de Telegram (Mirar en configuración de Telegram).

![](images_demo/telegram.png)
  
- Anuncios crawleados se guardan en un csv.
- Se muestra por terminal los productos.

![](images_demo/terminal_results.png)


- Que los productos se guarden a una base de datos con sus respectivos campos.





# Instalación

```shell
$ git clone https://github.com/KevinLiebergen/wallapop_crawler.git
$ cd wallapop_crawler
$ pip3 install virtualenv
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```

# Setup entorno

1. Mediante script instalación
```shell
$ cd setup
$ sh setup.sh
````

* Credenciales MySQL que se crean:
>  Usuario: walla_user <br> Contraseña: walla_password

2. Instalación Gecko driver paso por paso

```shell
$ wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
$ tar xvfz geckodriver-v0.24.0-linux64.tar.gz
$ sudo mv geckodriver /usr/local/bin
$ rm geckodriver-v0.24.0-linux64.tar.gz
```

# Ejecución

## Código


### Sin parámetros

Leer detenidamente la sección de __configuración Telegram__ y __conexión base de datos__ para saber si comentar o no esa parte del código. 

```shell
(venv) $ cd project
(venv) $ python3 main.py
```


### Con parámetros

```shell
$ python3 main.py --help
usage: main.py [-h] [--search SEARCH] [--min MIN] [--max MAX] [--limit LIMIT]
               [--teleg {s,n}]

Especifica opciones para el crawler

optional arguments:
  -h, --help       show this help message and exit
  --search SEARCH  Producto a buscar
  --min MIN        Define el precio minimo de la busqueda del producto
  --max MAX        Define el precio maximo de la busqueda del producto
  --limit LIMIT    Numero de productos que buscar por iteracion
  --teleg {s,n}    Envío de mensajes por Telegram
```

Ejemplo

```shell
$ python3 main.py --search bmw --min 10000 --max 10000 --limit 3 --teleg s
```

## Docker

* Instalar docker and docker-compose

```bash
# Docker
$ sudo apt install docker.io
# Docker-compose
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
$ sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

- Construcción de la imagen:
```bash
$ docker build . -t walla_crawler
```

- Ejecución de la imagen en modo interactivo:
  * Puentear fichero de configuración de Telegram (`-v`)

* En caso de que no se quieran enviar mensajes a Telegram omitir:
  * `-v $(pwd)/api_telegram.json:/crawler/project/outputs/api_telegram.json`

```bash
$ docker run --shm-size 2g -v $(pwd)/csvs:/crawler/csvs \
-v $(pwd)/api_telegram.json:/crawler/project/outputs/api_telegram.json \
-it walla_crawler
```

# Configuración Telegram

Este script implementa la opción de enviar los anuncios a un grupo privado de Telegram, te pregunta por teclado si quieres implementar este módulo, en caso afirmativo, lee del archivo `outputs/api_telegram.json`.



Para ello es necesario:

- Crear tu propio bot
    - Comienza una conversación con `@BotFather` y escribe `/newbot`. Especifica el nombre y el nickname
- Crear un grupo y añadir el bot creado
- Conocer el __token__ del bot creado (Botfather al crear tu bot te lo escribe por pantalla) y __dale valor a la variable token con el de tu bot__ en el fichero `api_telegram.json`.
- Conocer el __chat id__ del grupo creado y darle valor a la variable __ch_id__ en el fichero `api_telegram.json`.

<br>[Video resumen como crear tu bot y conocer tu token y chat id](https://www.youtube.com/watch?v=UhZtrhV7t3U)

# Conexión base de datos

__Por defecto,__ la instalación `setup.sh` realiza todo lo necesario para configurar la base de datos. Si ha ejecutado `setup.sh` correctamente no es necesario continuar con lo siguiente.

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

Una vez esté instalado, al ejecutar el script se creará la respectiva tabla de la base de datos y se guardarán las consultas en dicha base de datos. Si se quiere omitir comentar las llamadas a los métodos :

`guardar_elemento_bbdd(producto)` y `cursor, db = configurar_bbdd()` 

En las líneas 182 y 261 aproximadamente.

Si se desea acceder a la base de datos se accederá con:
<br>`$ mysql -u root -p`

La contraseña solicitada será __root__

# Salida entorno virtual

`(venv) $ deactivate`


# TO DO

* Args segundos entre búsquedas

* Docker-compose
  * Puentear salida de base de datos (`-v`)


```bash
$ docker-compose build
$ docker-compose run crawler
```
__No se puede hacer `$ docker-compose up` porque up no es interactivo, por eso hacemos run crawler__


<a href="https://www.buymeacoffee.com/kevinliebergen" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>