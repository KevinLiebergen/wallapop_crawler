from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import re
import time
import sys

# Preguntar junquera si va aqui o en el main
from outputs.telegram import Telegram
from outputs.csv import CSV
from outputs.db import BaseDatos
import outputs.informacion_pantalla


class Crawler:

    def __init__(self, options):
        self.driver = webdriver.Firefox(options=options)
        self.array_urls

    def gen_url(self, busqueda, precio_minimo, precio_maximo):
        # return "asbc%d" % (precio_maximo)
        # return "abasdfas{PM}".format(PM=precio_maximo)
        result = "https://es.wallapop.com/search?keywords=" + busqueda
        if precio_minimo:
            result += "&min_sale_price=" + str(precio_minimo)
        if precio_maximo:
            result += "&max_sale_price=" + str(precio_maximo)  # +"&latitude=40.4146500&longitude=-3.7004000
        return result

    def run(self, busqueda, prec_min, prec_max, num_max_productos):
        url = self.gen_url(self, busqueda, prec_min, prec_max)
        self.driver.get(url)

        self.aceptar_cookies()
        self.click_mas_productos()
        self.scroll_hasta_final()

        contador, array_urls = self.clickear_cada_producto(num_max_productos)

    def aceptar_cookies(self):
        # wait explicito que espera a que salga el popup de las cookies para aceptarlo
        try:
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".qc-cmp-button")))
            time.sleep(2)

            # Hace click en el boton aceptar cookies
            self.driver.find_elements_by_css_selector('.qc-cmp-button')[1].click()

        except TimeoutException:
            print("Tardando demasiado tiempo\n")

        except ElementNotInteractableException:
            print("No interactuable...")

    def click_mas_productos(self):
        if EC.presence_of_element_located((By.CSS_SELECTOR, ".Button")):
            boton_mas_productos = self.driver.find_element_by_css_selector('.Button')
            self.driver.execute_script("arguments[0].click();", boton_mas_productos)

    def scroll_hasta_final(self):
        scroll_pause_time = 1

        try:
            # Get scroll height
            last_height = self.driver.execute_script("return document.body.scrollHeight")

        except ElementNotInteractableException:
            print("No se puede hacer scroll down\n")
            self.driver.close()
            sys.exit(1)

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_product(self, product_link):

        localizacion = self.driver.find_element_by_css_selector('.card-product-detail-location').text.split(',')

        self.titulo = self.driver.find_elements_by_css_selector('.card-product-detail-title')[0].text
        self.precio = self.driver.find_elements_by_css_selector('.card-product-detail-price')[0].text
        self.descripcion = self.driver.find_elements_by_css_selector('.card-product-detail-description')[0].text
        # Para la localizacion se encuentra ciudad y barrio en una misma etiqueta, se separa por una coma, el
        # primer texto es el barrio y el segundo la ciudad (he puesto ultimo xq 1 daba error)
        self.barrio = localizacion[0]
        self.ciudad = localizacion[len(localizacion) - 1].lstrip()
        self.fechaPublicacion = self.driver.find_element_by_css_selector('.card-product-detail-user-stats-published').text
        self.puntuacion = self.driver.find_element_by_css_selector('.card-profile-rating').get_attribute("data-score")
        self.imagenURL = self.driver.find_element_by_css_selector(
            '#js-card-slider-main > li:nth-child(1) > img:nth-child(1)').get_attribute("src"),
        self.url = product_link

        return self

    def clickear_cada_producto(self, max_productos):
        producto = 0
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        for link in soup.find_all('a', href=re.compile('/item')):
            # TODO url.join
            product_link = "https://es.wallapop.com" + link['href']
            if product_link not in self.urls:
                self.driver.get("https://es.wallapop.com" + link['href'])
                p = self.get_product(product_link)

                informacion = outputs.informacion_pantalla.InformacionPantalla(p)
                informacion.imprimir_elementos()

                # telegram.enviar_mensajes_a_telegram(producto["url"])

                producto += 1

                self.urls += [product_link]
                if producto == max_productos:
                    break

        return producto

    def cerrar_navegador(self):
        self.driver.close()

