from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import telebot
import warnings
import json
import pymysql
import os
import crawler

class Vista:
    def __init__(self):
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

    def preguntar_busqueda(self):
        print("Especifique que buscar: ", end='')
        self.busqueda = input()

        # por defecto a para que se meta en el while y pregunta hasta conseguir s o n
        precio_boolean = 'a'

        while not (precio_boolean == 's' or precio_boolean == 'n'):
            print("¿Quieres filtrar los productos por precio? [s/n]: ", end='')
            precio_boolean = input()

        if precio_boolean == 's':
            print("Precio minimo: ", end='')
            self.precio_minimo = input()
            print("Precio maximo: ", end='')
            self.precio_maximo = input()
            self.url_busqueda = crawler.Crawler.gen_url(self.busqueda, self.precio_minimo, self.precio_maximo)

        else:
            self.url_busqueda = "https://es.wallapop.com/search?keywords=" + self.busqueda
            # +"&latitude=40.4146500&longitude=-3.7004000"

        return self.url_busqueda, self.busqueda


    def limitar_busqueda(self):
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


class Telegram:
    def __init__(self):
        with open('api_telegram.json') as json_file:
            data = json.load(json_file)

            self.token = data['token']
            self.ch_id = data['ch_id']
            self.tb = telebot.TeleBot(self.token)

    def enviar_mensajes_a_telegram(self, url):
        self.tb.send_message(self.ch_id, url)


class BaseDatos:
    def __init__(self):
        db_addr = os.environ.get('DB_ADDR', 'localhost')

        self.db = pymysql.connect(
            host=db_addr, port=3306, user="root",
            passwd="root", db="crawler"
        )
        self.cursor = self.db.cursor()

    def crear_nueva_tabla(self):
        # Creamos tabla nueva, nombre sin espacios
        crear_tabla = "CREATE TABLE productos (Titulo VARCHAR(50), Precio VARCHAR(30), " \
                        "Barrio INT, Ciudad VARCHAR(50), Fecha_publicacion VARCHAR(50), Puntuacion_vendedor float, " \
                        "Imagen VARCHAR(300), url VARCHAR(300), PRIMARY KEY (url))"

        try:
            # Suprime los warnings de mysql (util para cuando inserta filas duplicadas y no deja)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.cursor.execute(crear_tabla)

                self.db.commit()
        except:
            self.db.rollback()

    def guardar_elemento_bbdd(self, produc):

        query = "INSERT IGNORE INTO productos VALUES ( '" + produc["titulo"] + "', '" + \
                produc["precio"] + "', " + produc["barrio"] + ", '" + produc["ciudad"] + "', '" + \
                produc["fechaPublicacion"] + "', " + produc["puntuacion"] + ", '" + produc["imagenURL"] + "', '" + \
                produc["url"] + "')"

        try:
            # Suprime los warnings de mysql (util para cuando inserta filas duplicadas y no deja)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.cursor.execute(query)

                self.db.commit()
        except:
            self.db.rollback()


class CSV:
    def __init__(self, titulo_busqueda):
        self.titulo_busqueda = titulo_busqueda
        with open('csvs/' + self.titulo_busqueda + '.csv', 'w') as f:
            f.write("Titulo, Precio, Barrio, Ciudad, Fecha publicacion, Puntuacion vendedor, Imagen, URL \n")

    def escribir_a_csv(producto, titulo_busqueda):
        with open('csvs/' + titulo_busqueda + '.csv', 'a') as f:
            f.write(producto["titulo"] + "," + producto["precio"] + "," + producto["barrio"] + ","
                    + producto["ciudad"] + "," + producto["fechaPublicacion"] + ", " + producto["puntuacion"]
                    + "," + producto["imagenURL"] + "," + producto["url"] + "\n")


class WebDriver:
    def __init__(self):
        # Abre un navegador de Firefox y navega por la pagina web
        self.options = Options()
        # Modo headless
        self.options.headless = False

    def iniciar_firefox(self, url):
        self.driver = webdriver.Firefox(options=self.options)
        self.driver.get(url)

        return self.driver


class Producto:
    def __init__(self):
        localizacion = driver.find_element_by_css_selector('.card-product-detail-location').text.split(',')

        self.titulo = driver.find_elements_by_css_selector('.card-product-detail-title')[0].text
        self.precio = driver.find_elements_by_css_selector('.card-product-detail-price')[0].text
        self.descripcion = driver.find_elements_by_css_selector('.card-product-detail-description')[0].text
        # Para la localizacion se encuentra ciudad y barrio en una misma etiqueta, se separa por una coma, el
        # primer texto es el barrio y el segundo la ciudad (he puesto ultimo xq 1 daba error)
        self.barrio = localizacion[0]
        self.ciudad = localizacion[len(localizacion) - 1].lstrip()
        self.fechaPublicacion = driver.find_element_by_css_selector('.card-product-detail-user-stats-published').text
        self.puntuacion = driver.find_element_by_css_selector('.card-profile-rating').get_attribute("data-score")
        self.imagenURL = driver.find_element_by_css_selector(
            '#js-card-slider-main > li:nth-child(1) > img:nth-child(1)').get_attribute("src"),
        self.url = driver.current_url

        imprimir_elementos(self)

        csv_class.escribir_a_csv(self, vista.busqueda)

        # TODO Método dentro del crawler
        #guardar_elemento_bbdd(self)


def gen_url(busqueda, precio_minimo, precio_maximo):
    # return "asbc%d" % (precio_maximo)
    # return "abasdfas{PM}".format(PM=precio_maximo)
    return "https://es.wallapop.com/search?keywords=" + busqueda + "&min_sale_price=" + str(precio_minimo) + \
                          "&max_sale_price=" + str(precio_maximo)  # +"&latitude=40.4146500&longitude=-3.7004000


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


def run(url_busc, busqueda, num_max_productos):
    global driver # Esto como parametro de clase

    # Iniciar telegram
    t = Telegram()
    global csv_class
    csv_class = CSV(busqueda)

    # Inicia base de datos
    bbdd = BaseDatos()
    bbdd.crear_nueva_tabla()
    array_urls = [] # Esto como parametro de clase

    # Tiempo entre busquedas en segundos
    segundos_dormidos = 3600  # 3600 seg = 1 hora

    wd = WebDriver()

    while True:

        wdriver = wd.iniciar_firefox(url_busc)

        cr = crawler.Crawler(wdriver)

        cr.aceptar_cookies()
        cr.click_mas_productos()
        cr.scroll_hasta_final()
        contador, array_urls = cr.clickear_cada_producto(array_urls, num_max_productos, t)

        print(str(contador) + " nuevos productos encontrados")

        # Cierra el navegador
        driver.close()

        print("Esperando " + str(segundos_dormidos) + " segundos para volver a buscar")
        print("###########################")

        time.sleep(segundos_dormidos)

# def run(producto, n_productos):
#     pass
#
# def main():
#     producto = args.get('producto', 'default')
#     n_productos = args.get('n_productos', 5)
#     ...
#     run(producto, n_productos)
#
# def main_cli():
#     producto = input("Qué product quieres?")
#     ...
#     run(producto, n_productos)
# import argparse
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description="")
#
#     print(p)
#     if '--cli' in args:
#         main_cli()
#     else:
#         main()

driver = None


if __name__ == '__main__':

    # Instancia la clase, imprime wallapop crawler
    vista = Vista()

    # Pregunta que buscar y demas filtros
    if os.environ.get('CLI', None):
        url_buscar, producto_busqueda = vista.preguntar_busqueda()
        productos_limitar = vista.limitar_busqueda()
    else:
        producto_busqueda = os.environ.get('BUSQUEDA', 'bici enduro')
        url_buscar = gen_url(producto_busqueda, 2000, 2000)
        productos_limitar = int(os.environ.get('PRODUCTOS_LIMITAR', 5))

    run(url_buscar, producto_busqueda, productos_limitar)
