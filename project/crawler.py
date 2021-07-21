from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import logging
import datetime
import re
import time
import sys
import csv

from outputs import telegram
from outputs import save_csv
from outputs.db import BaseDatos


class Producto:
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
        res = "#" * 60
        res += "\nTitulo: %s" % self.titulo
        res += "\n" + "Precio: %s" % self.precio
        res += "\n" + "Descripción: %s" % self.descripcion
        res += "\n" + "Barrio: %s" % self.barrio
        res += "\n" + "Ciudad: %s" % self.ciudad
        res += "\n" + "Fecha publicación: %s" % self.fecha_publicacion
        res += "\n" + "Puntuación vendedor: %s" % self.puntuacion_vendedor
        res += "\n" + "Imagen: %s" % self.imagen
        res += "\n" + "URL: %s" % self.url
        return res


class Crawler:

    def __init__(self, options):
        self.driver = webdriver.Firefox(options=options)
        # self.driver = webdriver.Chrome(chrome_options=options)
        self.visited = []
        self.unprocessed = []
        self.known = []
        self.products_in_csv = []

        logging.basicConfig(level=20)

    def run(self, busqueda, instancia_teleg, prec_min, prec_max, database):
        teleg_obj = telegram.Telegram() if instancia_teleg else None

        fichero = save_csv.CSV(busqueda)

        if not fichero.fichero_nuevo:
            self.known = self.load_products_from_file(fichero)

        # while True:
        new_urls = 0

        url = self.gen_url(busqueda, prec_min, prec_max)
        self.driver.get(url)
        self.aceptar_cookies()
        self.click_mas_productos()
        self.scroll_hasta_final()

        # Devuelve todas las urls de la página que no estén en known (que no ha mirado ya)
        urls = self.get_product_urls()
        self.known += urls
        self.unprocessed += urls

        for i in range(len(self.unprocessed)):
            try:
                url = self.unprocessed.pop()
            except:
                print("#" * 60)
                print("No existen más productos, esperando...")
                break

            new_urls += 1
            p = self.get_product("https://es.wallapop.com" + url)

            self.visited.append(url)
            self.save_product(fichero, p, teleg_obj, database)

        # Guardo en DB(array_urls)
        print("[-] %d nuevos productos encontrados" % new_urls)

        # print("[-] Esperando %d segundos para volver a buscar" % sleep_time)
        now = datetime.datetime.now()
        print("{}".format(now.strftime("%d/%m/%Y, %H:%M:%S")))
        # time.sleep(sleep_time)
        print("#" * 50)
        self.driver.quit()

    def load_products_from_file(self, fichero):
        with open(fichero.fichero_csv) as file:
            csv_reader = csv.reader(file, delimiter=',')

            for n_line, row in enumerate(csv_reader):
                if n_line == 0:
                    continue
                self.products_in_csv.append(row[-1])

        return self.products_in_csv

    @staticmethod
    def gen_url(busqueda, precio_minimo, precio_maximo):
        # return "abasdfas{PM}".format(PM=precio_maximo)
        result = "https://es.wallapop.com/search?keywords=%s" % busqueda
        if precio_minimo:
            result += "&min_sale_price={}".format(precio_minimo)
        if precio_maximo:
            result += "&max_sale_price={}".format(precio_maximo)  # +"&latitude=40.4146500&longitude=-3.7004000
        return result

    def aceptar_cookies(self):
        # self.driver.execute_script('''
        #     document.addEventListener("DOMContentLoaded", function(){
        #         window.__cmpui("setAndSaveAllConsent", !0);
        #     });
        # ''')

        # wait explicito que espera a que salga el popup de las cookies para aceptarlo
        try:
            wait = WebDriverWait(self.driver, 20)

            # wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, ".qc-cmp-button")))

            # Updated v2.0
            wait.until(ec.presence_of_element_located((By.ID, "didomi-notice-agree-button")))
            time.sleep(2)

            # Hace click en el botón aceptar cookies
            # self.driver.find_elements_by_css_selector('.qc-cmp-button')[1].click()

            # Updated v2.0
            self.driver.find_element_by_id("didomi-notice-agree-button").click()
            print("[-] Cookies aceptadas")

        except TimeoutException:
            logging.error("No hay boton de aceptar cookies..\n")

        except ElementNotInteractableException:
            logging.error("No interactuable...")

    def click_mas_productos(self):
        # v1.0
        # if ec.presence_of_element_located((By.CSS_SELECTOR, ".Button")):
        #     boton_mas_productos = self.driver.find_element_by_css_selector('.Button')
        #     self.driver.execute_script("arguments[0].click();", boton_mas_productos)

        time.sleep(1)
        try:
            if ec.presence_of_element_located((By.ID, "more-products-btn")):
                self.driver.find_element_by_id("more-products-btn").click()
        except:
            print("[-] No se ha encontrado el botón de más productos")

    def scroll_hasta_final(self):
        scroll_pause_time = 2

        try:
            # Consigue la altura del scroll
            last_height = self.driver.execute_script("return document.body.scrollHeight")

        except:
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
        print("[-] Recolectando URLs de anuncios")
        res = set()
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        for link in soup.find_all('a', href=re.compile('/item')):
            if not any(link['href'] in url for url in self.known):
                # res.append(link['href'])
                res.add(link['href'])

        return list(res)

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
                            fecha_publicacion, puntuacion, imagen_url, url)

        return producto

    @staticmethod
    def save_product(fichero, product, t, datab):
        print("[-] Guardando producto {}".format(product.url))
        t.enviar_mensajes_a_telegram(product.url, product.precio) if t else None
        fichero.escribir_a_csv(product)

        print(product.__str__())

        if datab == 's':
            BaseDatos.guardar_elemento_bbdd()

    def get_product_info(self, product_link):
        p = self.get_product("https://es.wallapop.com" + product_link)
        print(p.__str__())

    def cerrar_navegador(self):
        self.driver.close()

# class DB(Pipeline):
#     def save(self, product):
#         "insert into product values %s" %(product)
