from selenium.webdriver.firefox.options import Options
import os
from crawler import Crawler
import logging


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


def run(nombre_producto, prec_min=0, prec_max=20000, num_max_productos=50):

    # Segundos entre busquedas
    segundos_dormidos = 60  # 3600 seg = 1 hora

    # Modo headless
    options = Options()
    options.headless = False
    c = Crawler(options)

    c.run(nombre_producto, prec_min, prec_max, num_max_productos, sleep_time=segundos_dormidos)


def main_cli():

    precio_min = None
    precio_max = None
    num_productos_limitar = None

    print("Especifique que buscar: ", end='')
    busqueda = input()

    while True:
        print("¿Quieres filtrar los productos por precio? [s/n]: ", end='')
        precio_boolean = input()

        if precio_boolean == 's':
            print("Precio minimo: ", end='')
            precio_min = input()
            print("Precio maximo: ", end='')
            precio_max = input()

            break

        elif precio_boolean == 'n':
            break

    while True:
        print("¿Limitar el número de productos? [s/n]: ", end='')
        limitar_boolean = input()
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

        elif limitar_boolean == 'n':
            break

    run(busqueda, int(precio_min), int(precio_max), int(num_productos_limitar))


def main():
    busqueda = os.environ.get('BUSQUEDA', 'bici enduro')
    precio_min = os.environ.get('PRECIO_MIN', 1100)
    precio_max = os.environ.get('PRECIO_MAX', 1400)
    productos_limitar = int(os.environ.get('PRODUCTOS_LIMITAR', 5))

    run(busqueda, precio_min, precio_max, productos_limitar)

# import argparse
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description="")
#
#     print(p)
#     if '--cli' in args:
#         main_cli()
#     else:
#         main()


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    saludar()
    # Si existe variable de entorno CLI, pregunta al usuario
    if os.environ.get('CLI', None):
        main_cli()
    # Si no lee los argumentos que le pasamos
    else:
        main()
