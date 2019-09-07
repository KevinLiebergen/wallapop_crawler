from selenium.webdriver.firefox.options import Options
import time
import os
from crawler import Crawler


# def imprime_elementos(self):
#     imprimir_elementos(self)
#     CSV.escribir_a_csv(self, busqueda)
#
#     # TODO Método dentro del crawler
#     #guardar_elemento_bbdd(self)



'''
PREGUNTAR A JUNQUERA SI LAS LLAMADAS A LA BD, TELEGRAM Y CSV SE HACEN 
DESDE EL MAIN O DESDE LA CLASE CRAWLER, AHORA ESTA EN CRAWLER

'''


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


def run(nombre_producto, prec_min, prec_max, num_max_productos):

    array_urls = []  # Esto como parametro de clase

    # Tiempo entre busquedas en segundos
    segundos_dormidos = 3600  # 3600 seg = 1 hora

    # Abre un navegador de Firefox y navega por la pagina web
    options = Options()
    # Modo headless
    options.headless = False
    c = Crawler(options)

    while True:
        contador, array_urls = c.run(nombre_producto, prec_min, prec_max, num_max_productos)

        print(str(contador) + " nuevos productos encontrados")

        c.cerrar_navegador()

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
