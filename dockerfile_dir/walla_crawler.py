from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import sys
import time
import re
import telebot
import warnings
import json
import pymysql


def imprimir_intro():
    # Diseño por http://patorjk.com/software/taag/
    print('''                                                                          
     (  (          (  (                                           (           
     )\))(   '   ) )\ )\   )                      (      ) (  (   )\  (  (    
    ((_)()\ ) ( /(((_|(_| /( `  )   (  `  )     ( )(  ( /( )\))( ((_)))\ )(   
    _(())\_)())(_))_  _ )(_))/(/(   )\ /(/(     )(()\ )(_)|(_)()\ _ /((_|()\  
    \ \((_)/ ((_)_| || ((_)_((_)_\ ((_|(_)_\   ((_|(_|(_)__(()((_) (_))  ((_) 
     \ \/\/ // _` | || / _` | '_ \) _ \ '_ \) / _| '_/ _` \ V  V / / -_)| '_| 
      \_/\_/ \__,_|_||_\__,_| .__/\___/ .__/  \__|_| \__,_|\_/\_/|_\___||_|   
                            |_|       |_|                                     
          ''')


def preguntar_busqueda():
    print("Especifique que buscar: ", end='')
    busqueda = input()

    # por defecto a para que se meta en el while y pregunta hasta conseguir s o n
    precio_boolean = 'a'

    while not (precio_boolean == 's' or precio_boolean == 'n'):
        print("¿Quieres filtrar los productos por precio? [s/n]: ", end='')
        precio_boolean = input()

    if precio_boolean == 's':
        print("Precio minimo: ", end='')
        precio_minimo = input()
        print("Precio maximo: ", end='')
        precio_maximo = input()

        url_busqueda = "https://es.wallapop.com/search?keywords=" + busqueda + "&min_sale_price=" + precio_minimo + \
                       "&max_sale_price=" + precio_maximo  # +"&latitude=40.4146500&longitude=-3.7004000"

    else:
        url_busqueda = "https://es.wallapop.com/search?keywords=" + busqueda
        # +"&latitude=40.4146500&longitude=-3.7004000"

    return url_busqueda, busqueda


def limitar_busqueda():
    # Igual que antes
    limitar_boolean = 'a'

    while not (limitar_boolean == 's' or limitar_boolean == 'n'):
        print("¿Limitar el número de productos? [s/n]: ", end='')
        limitar_boolean = input()

    if limitar_boolean == 's':
        num_productos_limitar = 0
        while not (num_productos_limitar > 0):
            print("Numero de productos a limitar [> 0]: ", end='')
            try:
                num_productos_limitar = int(input())
            except ValueError:
                num_productos_limitar = 0

    else:
        num_productos_limitar = 100

    print("###########################")
    return num_productos_limitar


def aceptar_cookies():
    # wait explicito que espera a que salga el popup de las cookies para aceptarlo
    try:
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".qc-cmp-button")))
        time.sleep(2)

        # Hace click en el boton aceptar cookies
        driver.find_elements_by_css_selector('.qc-cmp-button')[1].click()

    except TimeoutException:
        print("Tardando demasiado tiempo\n")

    except ElementNotInteractableException:
        print("No interactuable...")


def click_mas_productos():
    boton_mas_productos = driver.find_element_by_css_selector('.Button')
    driver.execute_script("arguments[0].click();", boton_mas_productos)


def scroll_hasta_final():
    scroll_pause_time = 1

    try:
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

    except ElementNotInteractableException:
        print("No se puede hacer scroll down\n")
        driver.close()
        sys.exit(1)

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def clickear_cada_producto(urls):
    producto = 0
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for link in soup.find_all('a', href=re.compile('/item')):

        if "https://es.wallapop.com" + link['href'] not in urls:
            driver.get("https://es.wallapop.com" + link['href'])

            extraer_elementos()
            producto += 1
            urls += ["https://es.wallapop.com" + link['href']]
            if producto == productos_limitar:
                break

    return producto, urls


def extraer_elementos():
    localizacion = driver.find_element_by_css_selector('.card-product-detail-location').text.split(',')

    diccionario_producto = {
        "titulo": driver.find_elements_by_css_selector('.card-product-detail-title')[0].text,
        "precio": driver.find_elements_by_css_selector('.card-product-detail-price')[0].text,
        "descripcion": driver.find_elements_by_css_selector('.card-product-detail-description')[0].text,
        # Para la localizacion se encuentra ciudad y barrio en una misma etiqueta, se separa por una coma, el
        # primer texto es el barrio y el segundo la ciudad (he puesto ultimo xq 1 daba error)
        "barrio": localizacion[0],
        "ciudad": localizacion[len(localizacion) - 1].lstrip(),
        "fechaPublicacion": driver.find_element_by_css_selector('.card-product-detail-user-stats-published').text,
        "puntuacion": driver.find_element_by_css_selector('.card-profile-rating').get_attribute("data-score"),
        "imagenURL": driver.find_element_by_css_selector(
            '#js-card-slider-main > li:nth-child(1) > img:nth-child(1)').get_attribute("src"),
        "url": driver.current_url
    }

    imprimir_elementos(diccionario_producto)


def imprimir_elementos(producto):
    print("Titulo: " + producto["titulo"])
    print("Precio: " + producto["precio"])
    print("Descripcion: " + producto["descripcion"])
    print("Barrio: " + producto["barrio"])
    print("Ciudad: " + producto["ciudad"])
    print("Fecha publicacion: " + producto["fechaPublicacion"])
    print("Puntuacion vendedor: " + producto["puntuacion"])
    print("Imagen: " + producto["imagenURL"])
    print("URL: " + producto["url"])
    print("###########################")

    enviar_mensajes_a_telegram(producto["url"])
    escribir_a_csv(producto, busqueda)
    guardar_elemento_bbdd(producto)


def configurar_bbdd():
    db = pymysql.connect(
        host="localhost", port=3306, user="root",
        passwd="root", db="crawler"
    )
    cursor = db.cursor()

    # Creamos tabla nueva, nombre sin espacios
    crear_tabla = "CREATE TABLE " + busqueda.replace(" ", "") + " (Titulo VARCHAR(50), Precio VARCHAR(30), " \
                   "Barrio INT, Ciudad VARCHAR(50), Fecha_publicacion VARCHAR(50), Puntuacion_vendedor float, " \
                   "Imagen VARCHAR(300), url VARCHAR(300), PRIMARY KEY (url))"

    try:
        # Suprime los warnings de mysql (util para cuando inserta filas duplicadas y no deja)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cursor.execute(crear_tabla)

            db.commit()
    except:
        db.rollback()

    return cursor, db


def guardar_elemento_bbdd(produc):

    query = "INSERT IGNORE INTO " + busqueda.replace(" ", "") + " VALUES ( '" + produc["titulo"] + "', '" + \
            produc["precio"] + "', " + produc["barrio"] + ", '" + produc["ciudad"] + "', '" + \
            produc["fechaPublicacion"] + "', " + produc["puntuacion"] + ", '" + produc["imagenURL"] + "', '" + \
            produc["url"] + "')"

    try:
        # Suprime los warnings de mysql (util para cuando inserta filas duplicadas y no deja)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cursor.execute(query)

            db.commit()
    except:
        db.rollback()


def configurar_telegram():
    with open('api_telegram.json') as json_file:
        data = json.load(json_file)

        token = data['token']
        ch_id = data['ch_id']

        tb = telebot.TeleBot(token)

    return tb, ch_id


def enviar_mensajes_a_telegram(url):
    telebot.send_message(chat_id, url)


def cabecera_csv(titulo_busqueda):
    with open('csvs/' + titulo_busqueda + '.csv', 'w') as f:
        f.write("Titulo, Precio, Barrio, Ciudad, Fecha publicacion, Puntuacion vendedor, Imagen, URL \n")


def escribir_a_csv(producto, titulo_busqueda):
    with open('csvs/' + titulo_busqueda + '.csv', 'a') as f:
        f.write(producto["titulo"] + "," + producto["precio"] + "," + producto["barrio"] + ","
                + producto["ciudad"] + "," + producto["fechaPublicacion"] + ", " + producto["puntuacion"]
                + "," + producto["imagenURL"] + "," + producto["url"] + "\n")


array_urls = []

# Pregunta que buscar y demas filtros
imprimir_intro()
buscar, busqueda = preguntar_busqueda()
productos_limitar = limitar_busqueda()

# Iniciar telegram, base de datos
telebot, chat_id = configurar_telegram()
cursor, db = configurar_bbdd()

cabecera_csv(busqueda)

# Tiempo entre busquedas en segundos
segundos_dormidos = 3600  # 3600 seg = 1 hora

while True:
    # Abre un navegador de Firefox y navega por la pagina web

    options = Options()
    # Modo headless
    options.headless = False
    driver = webdriver.Firefox(options=options)

    driver.get(buscar)

    aceptar_cookies()
    click_mas_productos()
    scroll_hasta_final()
    contador, array_urls = clickear_cada_producto(array_urls)

    print(str(contador) + " nuevos productos encontrados")

    # Cierra el navegador
    driver.close()

    print("Esperando " + str(segundos_dormidos) + " segundos para volver a buscar")
    print("###########################")

    time.sleep(segundos_dormidos)
