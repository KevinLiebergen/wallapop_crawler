from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import os
from outputs import telegram
from outputs import csv



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

    def imprime_elementos(self):
        imprimir_elementos(self)
        csv_class.escribir_a_csv(self, busqueda)

        # TODO Método dentro del crawler
        #guardar_elemento_bbdd(self)


def saludar():
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


def run(busqueda, prec_min, prec_max, num_max_productos):
    # Iniciar telegram
    t = Telegram()

    csv_class = CSV(busqueda)

    # Inicia base de datos
    bbdd = BaseDatos()
    bbdd.crear_nueva_tabla()
    array_urls = [] # Esto como parametro de clase

    # Tiempo entre busquedas en segundos
    segundos_dormidos = 3600  # 3600 seg = 1 hora


    # Abre un navegador de Firefox y navega por la pagina web
    options = Options()
    # Modo headless
    options.headless = False
    c = Cralwer(options)

    while True:
        c.run(busqueda, prec_min, prec_max, num_max_productos)

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
    # Pregunta que buscar y demas filtros
    if os.environ.get('CLI', None):
        print("Especifique que buscar: ", end='')
        busqueda = input()

        # por defecto a para que se meta en el while y pregunta hasta conseguir s o n
        precio_boolean = 'a'

        while not (precio_boolean == 's' or precio_boolean == 'n'):
            print("¿Quieres filtrar los productos por precio? [s/n]: ", end='')
            precio_boolean = input()

        if precio_boolean == 's':
            print("Precio minimo: ", end='')
            precio_min = input()
            print("Precio maximo: ", end='')
            precio_max = input()
        productos_limitar = 5
    else:
        busqueda = os.environ.get('BUSQUEDA', 'bici enduro')
        precio_min = os.environ.get('PRECIO_MIN', None)
        precio_max = os.environ.get('PRECIO_MAX', None)
        productos_limitar = int(os.environ.get('PRODUCTOS_LIMITAR', 5))

    run(busqueda, precio_min, precio_max, productos_limitar)
