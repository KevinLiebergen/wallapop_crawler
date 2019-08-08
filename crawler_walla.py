from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
import sys

from bs4 import BeautifulSoup
import time

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

# Abre un navegador de Firefox y navega por la pagina web
driver = webdriver.Firefox()


driver.get("https://es.wallapop.com/search?catIds=17000&kws=motos")
#driver.get("https://es.wallapop.com/coches-segunda-mano")


# wait explicito que espera a que salga el popup de las cookies para aceptarlo, espera a que salga el popup
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".qc-cmp-button")))

    # Hace click en el boton aceptar cookies
    driver.find_element_by_css_selector('.qc-cmp-button').click()

except TimeoutException:
    print("Tardando demasiado tiempo\n")


# try catch para hacer scroll down
try:
    # Scroll hacia abajo para que se carguen todos los anuncios
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

except ElementNotInteractableException:
    print("No se puede hacer scroll down\n")
    driver.close()
    sys.exit(1)



print(driver.title)
print("-------------------------------------")


#time.sleep(5)


# Extrae los elementos basados en los css
titulo = driver.find_elements_by_css_selector('.product-info-title')
precio = driver.find_elements_by_css_selector('.product-info-price')
descripcion = driver.find_elements_by_css_selector('.product-info-description')

# Imprime los elementos
num_page_items = len(titulo)

for i in range(num_page_items):
    print("Titulo: " + titulo[i].text)
    print("Precio: " + precio[i].text)
    print("Descripcion: " + descripcion[i].text)
    print("###########################")



''' Escribir a csv
with open('resultado.csv','a') as f:
    f.write("Titulo, precio, descripcion \n")
    for i in range(num_page_items):
        f.write(titulo[i].text + "," + precio[i].text + ", " + descripcion[i].text + "\n")
'''

''' soup
soup = BeautifulSoup(driver.page_source, 'html.parser')

for link in soup.find_all('a'):
    print(link.get('href'))
'''

# Cierra el navegador
driver.close()
