from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import walla_crawler
from bs4 import BeautifulSoup
import re
import time
import sys


class Crawler:

    def __init__(self, driver):
        self.driver = driver

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

    def clickear_cada_producto(self, urls, max_productos, telegram):
        producto = 0
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        for link in soup.find_all('a', href=re.compile('/item')):

            if "https://es.wallapop.com" + link['href'] not in urls:
                self.driver.get("https://es.wallapop.com" + link['href'])

                p = walla_crawler.Producto()

                p.imprime_elementos()

                telegram.enviar_mensajes_a_telegram(producto["url"])

                producto += 1
                urls += ["https://es.wallapop.com" + link['href']]
                if producto == max_productos:
                    break

        return producto, urls

