from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
import sys
import time

from bs4 import BeautifulSoup


def imprimir_intro():
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


def aceptar_cookies():
    # wait explicito que espera a que salga el popup de las cookies para aceptarlo
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".qc-cmp-button")))
        time.sleep(2)

        # Hace click en el boton aceptar cookies
        driver.find_element_by_css_selector('.qc-cmp-button').click()

    except TimeoutException:
        print("Tardando demasiado tiempo\n")

    except ElementNotInteractableException:
        print("Error interno, cerrando...")
        driver.close()
        sys.exit(1)


def click_mas_productos():
    boton_mas_prod = driver.find_element_by_css_selector('.Button')
    driver.execute_script("arguments[0].click();", boton_mas_prod)


def scroll_hasta_final():
    SCROLL_PAUSE_TIME = 1

    try:
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

    except ElementNotInteractableException:
        print("No se puede hacer scroll down\n")
        driver.close()
        sys.exit(1)

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def imprimir_elementos():
    num_page_items = len(titulo)

    for i in range(num_page_items):
        print("Titulo: " + titulo[i].text)
        print("Precio: " + precio[i].text)
        print("Descripcion: " + descripcion[i].text)
        print("###########################")


def escribir_a_csv():
    with open('resultado.csv', 'a') as f:
        f.write("Titulo, precio, descripcion \n")
        for i in range(num_page_items):
            f.write(titulo[i].text + "," + precio[i].text + ", " + descripcion[i].text + "\n")


num_page_items = 0

imprimir_intro()

# Abre un navegador de Firefox y navega por la pagina web
driver = webdriver.Firefox()
#driver.get("https://es.wallapop.com/search?catIds=17000&kws=motos")
driver.get("https://es.wallapop.com/search?keywords=compiladores&latitude=40.4893538&longitude=-3.6827461")


aceptar_cookies()

click_mas_productos()

scroll_hasta_final()

# Extrae los elementos basados en los css
titulo = driver.find_elements_by_css_selector('.product-info-title')
precio = driver.find_elements_by_css_selector('.product-info-price')
descripcion = driver.find_elements_by_css_selector('.product-info-description')


imprimir_elementos()

#escribir_a_csv()

'''soup
soup = BeautifulSoup(driver.page_source, 'html.parser')

for link in soup.find_all('a'):
    print(link.get('href'))
'''


# Cierra el navegador
driver.close()
