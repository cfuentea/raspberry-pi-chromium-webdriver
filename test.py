#!/usr/bin/python3
from random import randint
from time import sleep
from datetime import datetime
from selenium import webdriver
from pyvirtualdisplay import Display
from pymongo import MongoClient
import socket, json, requests, io

# conexion a la base de datos
try:
    client = MongoClient('mongodb+srv://<usuario>:<password>@<hostname>/?retryWrites=true&w=majority')

# error en caso de no poder conectar
except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)

db = client.Cluster0

collection = db["sitiosWeb"]

# formato normalizado de fecha
hoy = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

# nombre del servidor (sonda) que correra el script
server_name = socket.gethostname()

# url de donde se obtendra los sitios web a revisar
url = 'https://raw.githubusercontent.com/cfuentea/raspberry-pi-chromium-webdriver/master/sitios.txt'

# parametros de visualizacion para desplegar la web
display = Display(visible=0, size=(1280, 760))
display.start()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-extensions')
#chrome_options.add_argument('--disable-dev-shm-usage')

# version script ejecutado en ontenedor
driver = webdriver.Chrome(options=chrome_options)
#driver.implicitly_wait(10)

def prueba_medicion(driver, web, server_name, hoy):
    try:
        web = web.strip()
        driver.get(web)
        navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
        responseStart = driver.execute_script("return window.performance.timing.responseStart")
        domComplete = driver.execute_script("return window.performance.timing.domComplete")
        backendPerformance_calc = (responseStart - navigationStart)/1000
        frontendPerformance_calc = (domComplete - responseStart)/1000
        data_dict = {
                "server_name": server_name,
                "timestamp": hoy,
                "url": web,
                "t_backend_seg": backendPerformance_calc,
                "t_frontend_seg": frontendPerformance_calc
            }
        driver.implicitly_wait(10)
        return data_dict
    except selenium.common.exceptions.WebDriverException as e:
        print(f'Ocurrio un error al acceder a la {web}: {str(e)}')
        return None

# espera variable para evitar parecer un robot
sleep(randint(5,30))

try:
    response = requests.get(url)
    response.raise_for_status()
except (requests.RequestException, ValueError):
    with open('/tmp/sitios.txt','r') as archivo:
        for web in archivo:
            try:
                data_dict = prueba_medicion(driver, web, server_name, hoy)
            except selenium.common.exceptions.WebDriverException as e:
                print(f'Ocurrio un error al cargar la pagina: {e}')
                data_dict = prueba_medicion(driver, web, server_name, hoy)
            collection.insert_one(data_dict)
else:
    for web in io.StringIO(response.text):
        try:
            data_dict = prueba_medicion(driver, web, server_name, hoy)
        except selenium.common.exceptions.WebDriverException as e:
            print(f'Ocurrio un error al cargar la pagina: {e}')
            data_dict = prueba_medicion(driver, web, server_name, hoy)
        collection.insert_one(data_dict)
finally:
    driver.quit()
    display.stop()
    client.close()
