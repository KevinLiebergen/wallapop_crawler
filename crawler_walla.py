from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
import sys
import time
import re
import telebot

from bs4 import BeautifulSoup


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


def preguntarBusqueda():
    print("Especifique que buscar: ", end='')
    busqueda = input()

    # print("Limite de kilometros a buscar (50000 max)")
    # distancia = int(input())

    print("¿Quieres filtrar los productos por precio? [s/n]: ", end='')
    precio_boolean = input()

    while not(precio_boolean == 's' or precio_boolean == 'n' ):
        print("¿Quieres filtrar los productos por precio? [s/n]: ", end='')
        precio_boolean = input()

    if precio_boolean == 's':
        print("Precio minimo: ", end='')
        precio_minimo = input()
        print("Precio maximo: ", end='')
        precio_maximo = input()

        url_busqueda = "https://es.wallapop.com/search?keywords="+busqueda+"&min_sale_price="+precio_minimo +\
                       "&max_sale_price="+precio_maximo     # +"&latitude=40.4146500&longitude=-3.7004000"

    else:
        url_busqueda = "https://es.wallapop.com/search?keywords="+busqueda
        # +"&latitude=40.4146500&longitude=-3.7004000"

    print("###########################")

    return url_busqueda


def aceptar_cookies():
    # wait explicito que espera a que salga el popup de las cookies para aceptarlo
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".qc-cmp-button")))
        time.sleep(2)

        # Hace click en el boton aceptar cookies
        driver.find_element_by_css_selector('.qc-cmp-button').click()

    except TimeoutException:
        print("Tardando demasiado tiempo\n")

    except ElementNotInteractableException:
        print("Error interno, cerrando...")
        driver.close()
        sys.exit(1)


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


def clickear_cada_producto():
    producto = 0
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for link in soup.find_all('a', href=re.compile('/item')):
        driver.get("https://es.wallapop.com" + link['href'])

        extraer_elementos()
        producto += 1

    return producto


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
        "imagenURL": driver.find_element_by_css_selector('#js-card-slider-main > li:nth-child(1) > img:nth-child(1)').get_attribute("src"),
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


def configurar_telegram():
    token = ' '
    ch_id = ' '
    tb = telebot.TeleBot(token)

    return tb, ch_id


def enviar_mensajes_a_telegram(url):

    telebot.send_message(chat_id, url)


def escribir_a_csv(producto):
    with open('resultado.csv', 'a') as f:
        f.write("Titulo, precio, descripcion \n")
        for i in range(len(producto["titulo"])):
            f.write(producto["titulo"][i].text+"," + producto["precio"][i].text + ", "
                    + producto["descripcion"][i].text + "\n")


telebot, chat_id = configurar_telegram()
imprimir_intro()
buscar = preguntarBusqueda()

# Abre un navegador de Firefox y navega por la pagina web
driver = webdriver.Firefox()
driver.get(buscar)

aceptar_cookies()
click_mas_productos()
scroll_hasta_final()
contador = clickear_cada_producto()

# escribir_a_csv(productos)

print(str(contador) + " productos encontrados")

# Cierra el navegador
driver.close()
