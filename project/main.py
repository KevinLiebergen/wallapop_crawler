

from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.chrome.options import Options

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


def run(nombre_producto, bool_teleg, modo_headless, seg_dormidos, db, prec_min=0, prec_max=20000):

    # Segundos entre búsquedasgg
    segundos_dormidos = seg_dormidos  # 3600 seg = 1 hora

    options = Options()
    # Modo headless
    options.headless = False if modo_headless == 'n' else True

    crawl = Crawler(options)

    crawl.run(nombre_producto, bool_teleg, prec_min, prec_max, db, sleep_time=segundos_dormidos)


def main_cli():

    global segs_espera
    global def_db

    print("Especifique que buscar: ", end='')
    busqueda = input()

    while True:
        print("¿Quieres filtrar los productos por precio? [s/n]: ", end='')
        precio_boolean = input()

        if precio_boolean == 's':
            print("Precio mínimo: ", end='')
            precio_min = input()
            print("Precio máximo: ", end='')
            precio_max = input()

            break

        elif precio_boolean == 'n':
            precio_min = 0
            precio_max = 20000
            break

    while True:
        print("¿Quieres enviar mensajes a un grupo de Telegram? [s/n]: ", end='')
        enviar_mensajes = input()

        if enviar_mensajes == 's':
            instancia_teleg = True
            break
        elif enviar_mensajes == 'n':
            instancia_teleg = False
            break

    while True:
        print("¿Quieres poner headless mode? (Sin interfaz) [s/n]: ", end='')
        modo_headless = input()

        if modo_headless == 's' or modo_headless == 'n':
            break

    while True:
        print("¿Quieres configurar tiempo entre búsquedas? (Por defecto %s segundos) [s/n]: " % segs_espera, end='')
        config_tiempo = input()

        if config_tiempo == 's':
            print("Segundos entre búsquedas: ", end='')
            segs_espera = int(input())
            break
        elif config_tiempo == 'n':
            break

    while True:
        print("¿Quieres guardar productos en la base de datos? (Por defecto {}) [s/n]: ".format(def_db),
              end='')
        database = input()

        if database == 's' or database == 'n':
            break

    run(busqueda, instancia_teleg, modo_headless, segs_espera, database,
        precio_min, precio_max, int(num_productos_limitar))


def main(argumentos):

    busqueda = f'{argumentos.search}'
    precio_min = argumentos.min
    precio_max = argumentos.max
    teleg = argumentos.teleg
    modo_headless = argumentos.headless
    segs_espera = argumentos.segs_espera
    database = argumentos.db

    run(busqueda, teleg, modo_headless, segs_espera, database, precio_min, precio_max)


if __name__ == '__main__':

    segs_espera = 600
    def_db = 'n'

    parser = argparse.ArgumentParser(description='Especifica opciones para el crawler')

    parser.add_argument('--search', required=False, help="Producto a buscar")
    parser.add_argument('--min', type=int, required=False, help="Define el precio mínimo de la búsqueda del producto")
    parser.add_argument('--max', type=int, required=False, help="Define el precio máximo de la búsqueda del producto")
    parser.add_argument('--teleg', required=False, help="Envío de mensajes por Telegram (activado por defecto)",
                        default="s", choices=['s', 'n'])
    parser.add_argument('--headless', required=False, help="Modo headless (sin interfaz)", default="n",
                        choices=['s', 'n'])
    parser.add_argument('--db', required=False, help="Conexión a base de datos[s/n]",
                        default=def_db, choices=['s', 'n'])

    parser.add_argument('--segs_espera', required=False, help="Segundos espera entre búsquedas (" + str(segs_espera) +
                                                              " segundos  por defecto)", default=segs_espera, type=int)

    args = parser.parse_args()

    saludar()

    # Si no lee los argumentos que le pasamos
    if args.search:
        main(args)
    # Si existe variable de entorno CLI, pregunta al usuario
    else:
        main_cli()
