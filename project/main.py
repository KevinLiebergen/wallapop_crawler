from selenium.webdriver.firefox.options import Options
from crawler import Crawler
import argparse


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
                            |_|       |_|      made with <3 by KevinLiebergen                 
          ''')


def run(nombre_producto, bool_teleg, prec_min=0, prec_max=20000, num_max_productos=50):

    # Segundos entre busquedas
    segundos_dormidos = 60  # 3600 seg = 1 hora

    # Modo headless
    options = Options()
    options.headless = False
    c = Crawler(options)

    c.run(nombre_producto, bool_teleg, prec_min, prec_max, num_max_productos, sleep_time=segundos_dormidos)


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
            precio_min = 0
            precio_max = 20000
            break

    while True:
        print("¿Limitar el número de productos? [s/n]: ", end='')
        limitar_boolean = input()

        if limitar_boolean == 's':
            num_productos_limitar = 0
            while not (num_productos_limitar > 0):
                print("Numero de productos a limitar [> 0]: ", end='')
                try:
                    num_productos_limitar = int(input())
                    break
                except ValueError:
                    num_productos_limitar = 0
            break

        elif limitar_boolean == 'n':
            num_productos_limitar = 50
            break

    while(True):
        print("¿Quieres enviar mensajes a un grupo de Telegram? [s/n]", end='')
        enviar_mensajes = input()

        if enviar_mensajes == 's':
            instancia_teleg = True
            break
        elif enviar_mensajes == 'n':
            instancia_teleg = False
            break

    run(busqueda, instancia_teleg, precio_min, precio_max, int(num_productos_limitar))


def main(argumentos):

    busqueda = f'{argumentos.search}'
    precio_min = argumentos.min
    precio_max = argumentos.max
    productos_limitar = argumentos.limit
    teleg = argumentos.teleg

    run(busqueda, teleg, precio_min, precio_max, productos_limitar)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Especifica opciones para el crawler')

    parser.add_argument('--search', required=False, help="Producto a buscar")
    parser.add_argument('--min', type=int, required=False, help="Define el precio minimo de la busqueda del producto")
    parser.add_argument('--max', type=int, required=False, help="Define el precio maximo de la busqueda del producto")
    parser.add_argument('--limit', type=int, required=False, help="Numero de productos que buscar por iteracion")
    parser.add_argument('--teleg', required=False, help="Envío de mensajes por Telegram", default="s", choices=['s', 'n'])

    args = parser.parse_args()

    saludar()

    # Si no lee los argumentos que le pasamos
    if args.search:
        main(args)
    # Si existe variable de entorno CLI, pregunta al usuario
    else:
        main_cli()
