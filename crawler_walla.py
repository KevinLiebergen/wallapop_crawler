from selenium import webdriver
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


with open('result.csv', 'w') as f:
    f.write("Anuncios ")

# Open up a Firefox browser and navigate to web page
driver = webdriver.Firefox()
driver.get("https://es.wallapop.com/search?catIds=17000&kws=enduro")

'''
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "myD"))
    )
finally:
    driver.quit()
'''

print(driver.title)

# Extract elements based on css
titulo = driver.find_elements_by_css_selector('.product-info-title')
precio = driver.find_elements_by_css_selector('.product-info-price')
descripcion = driver.find_elements_by_css_selector('.product-info-description')

# Print all elements
num_page_items = len(titulo)

for i in range(num_page_items):
    print("###########################")
    print("Titulo: " + titulo[i].text)
    print("Precio: " + precio[i].text)
    print("Descripcion: " + descripcion[i].text)

# Close browser once task is completed
driver.close()
