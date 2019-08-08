from selenium import webdriver
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Diseño por http://patorjk.com/software/taag/
from setuptools.command.install import install

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


with open('resultado.csv','w') as f:
    f.write("Titulo, precio, descripcion \n")



# Abre un navegador de Firefox y navega por la pagina web
driver = webdriver.Firefox()
#driver.get("https://es.wallapop.com/search?catIds=17000&kws=enduro")
driver.get("https://es.wallapop.com/coches-segunda-mano")

print(driver.title)
print("-------------------------------------")


time.sleep(10)


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

'''
with open('resultado.csv','a') as f:
    for i in range(num_page_items):
        f.write(titulo[i].text + "," + precio[i].text + ", " + descripcion[i].text + "\n")
'''

# Cierra el navegador
driver.close()
