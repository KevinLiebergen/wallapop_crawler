from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import logging
import re
import time
import sys

from outputs import telegram
from outputs import csv
from outputs.db import BaseDatos


class Producto:
    # def __init__(self, producto):
    def __init__(self, titulo, precio, descripcion, barrio, ciudad, fecha_publicacion,
                 puntuacion_vendedor, imagen, url):

        self.titulo = titulo
        self.precio = precio
        self.descripcion = descripcion
        self.barrio = barrio
        self.ciudad = ciudad
        self.fecha_publicacion = fecha_publicacion
        self.puntuacion_vendedor = puntuacion_vendedor
        self.imagen = imagen
        self.url = url

    def __str__(self):
        res = "Titulo: %s" % self.titulo
        res += "\n" + "Precio: %s" % self.precio
        res += "\n" + "Descripcion: %s" % self.descripcion
        res += "\n" + "Barrio: %s" % self.barrio
        res += "\n" + "Ciudad: %s" % self.ciudad
        res += "\n" + "Fecha publicacion: %s" % self.fecha_publicacion
        res += "\n" + "Puntuacion vendedor: %s" % self.puntuacion_vendedor
        res += "\n" + "Imagen: %s" % self.imagen
        res += "\n" + "URL: %s" % self.url
        res += "\n" + "#"*32
        return res


class Crawler:

    def __init__(self, options):
        self.driver = webdriver.Firefox(options=options)
        self.visited = []
        self.unprocessed = []
        self.known = []
#        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

    def run(self, busqueda, prec_min, prec_max, num_max_productos, sleep_time=3600):
        fichero = csv.CSV(busqueda)
        t = telegram.Telegram()

        while True:
            new_urls = 0

            url = self.gen_url(busqueda, prec_min, prec_max)
            self.driver.get(url)
            self.aceptar_cookies()
            self.click_mas_productos()
            self.scroll_hasta_final()

            # Devuelve todas las urls de la página que no estén en known
            urls = self.get_product_urls()
            self.known += urls
            # inserta urls ya insertadas antes, preguntar junquera si es necesario
            # usar un set
            self.unprocessed += urls
            for i in range(num_max_productos):
                url = self.unprocessed.pop()
                if not url:
                    break
                new_urls += 1
                p = self.get_product("https://es.wallapop.com" + url)

                self.visited.append(url)
                self.save_product(fichero, p, t)

            # Aqui guardo en DB(array_urls)
            logging.info(" %d nuevos productos encontrados" % new_urls)

            logging.info("Esperando %d segundos para volver a buscar" % sleep_time)
            logging.info("#"*16)

            time.sleep(sleep_time)

    def gen_url(self, busqueda, precio_minimo, precio_maximo):
        # return "asbc%d" % (precio_maximo)
        # return "abasdfas{PM}".format(PM=precio_maximo)
        result = "https://es.wallapop.com/search?keywords=%s" % busqueda
        if precio_minimo:
            result += "&min_sale_price=%d" % precio_minimo
        if precio_maximo:
            result += "&max_sale_price=%d" % precio_maximo  # +"&latitude=40.4146500&longitude=-3.7004000
        return result

    def aceptar_cookies(self):
        # wait explicito que espera a que salga el popup de las cookies para aceptarlo
        try:
            wait = WebDriverWait(self.driver, 20)
            wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, ".qc-cmp-button")))
            time.sleep(2)

            # Hace click en el boton aceptar cookies
            self.driver.find_elements_by_css_selector('.qc-cmp-button')[1].click()

        except TimeoutException:
            logging.error("Tardando demasiado tiempo\n")

        except ElementNotInteractableException:
            logging.error("No interactuable...")

    def click_mas_productos(self):
        if ec.presence_of_element_located((By.CSS_SELECTOR, ".Button")):
            boton_mas_productos = self.driver.find_element_by_css_selector('.Button')
            self.driver.execute_script("arguments[0].click();", boton_mas_productos)

    def scroll_hasta_final(self):
        scroll_pause_time = 1

        try:
            # Consigue la altura del scroll
            last_height = self.driver.execute_script("return document.body.scrollHeight")

        except ElementNotInteractableException:
            logging.error("No se puede hacer scroll down\n")
            self.driver.close()
            sys.exit(1)

        while True:
            # Scroll down hasta el final
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Espera a que cargue la pagina
            time.sleep(scroll_pause_time)

            # Calcula la nueva altura del scroll y lo compara con la anterior
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_product_urls(self):
        res = []
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        for link in soup.find_all('a', href=re.compile('/item')):
            res.append(link['href'])
        return res

    def get_product(self, product_link):

        self.driver.get(product_link)

        titulo = self.driver.find_elements_by_css_selector('.card-product-detail-title')[0].text
        precio = self.driver.find_elements_by_css_selector('.card-product-detail-price')[0].text
        descripcion = self.driver.find_elements_by_css_selector('.card-product-detail-description')[0].text
        # Para la localizacion se encuentra ciudad y barrio en una misma etiqueta, se separa por una coma, el
        # primer texto es el barrio y el segundo la ciudad (he puesto ultimo xq 1 daba error)
        localizacion = self.driver.find_element_by_css_selector('.card-product-detail-location').text.split(',')
        barrio = localizacion[0]
        ciudad = localizacion[len(localizacion) - 1].lstrip()
        fecha_publicacion = self.driver.find_element_by_css_selector('.card-product-detail-user-stats-published').text
        puntuacion = self.driver.find_element_by_css_selector('.card-profile-rating').get_attribute("data-score")
        imagen_url = self.driver.find_element_by_css_selector(
            '#js-card-slider-main > li:nth-child(1) > img:nth-child(1)').get_attribute("src"),
        url = product_link

        producto = Producto(titulo, precio, descripcion, barrio, ciudad,
                            fecha_publicacion,  puntuacion, imagen_url, url)

        return producto

    def save_product(self, fichero, product, t):
        t.enviar_mensajes_a_telegram(product.url)
        fichero.escribir_a_csv(product)

        print(product.__str__())
        # TODO  GET_PRODUCT_INFO()

        # for pipeline in self.pipelines:
        #     pipeline.save(product)
        # # telegram.enviar_mensajes_a_telegram(producto["url"])
        # # enviar a bd??
        # pass

    def get_product_info(self, product_link):
        p = self.get_product("https://es.wallapop.com" + product_link)
        print(p.__str__())

    def cerrar_navegador(self):
        self.driver.close()


# class Telegram(Pipeline):
#     def save(self, product):
#         tg.send(product)
#
# class DB(Pipeline):
#     def save(self, product):
#         "insert into product values %s" %(product)
