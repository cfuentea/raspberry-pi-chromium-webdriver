#!/usr/bin/python3
from random import randint
from time import sleep
from datetime import datetime
from selenium import webdriver
from pyvirtualdisplay import Display
import socket, requests, io

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

# version script ejecutado en ontenedor
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)

# espera variable para evitar parecer un robot
sleep(randint(5,30))

try:
    response = requests.get(url)
    response.raise_for_status()
except (requests.RequestException, ValueError):
    with open('/tmp/sitios.txt','r') as archivo:
        for web in archivo:
            web = web.strip()
            driver.get(web)
            navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
            responseStart = driver.execute_script("return window.performance.timing.responseStart")
            domComplete = driver.execute_script("return window.performance.timing.domComplete")
            backendPerformance_calc = (responseStart - navigationStart)/1000
            frontendPerformance_calc = (domComplete - responseStart)/1000
            data = f'{{"server_name":"{server_name}","timestamp":"{hoy}","url":"{web}","t_backend_seg":"{backendPerformance_calc}","t_frontend_seg":"{frontendPerformance_calc}"}}'
            print('opcion A: ' + data)
else:
    for web in io.StringIO(response.text):
        web = web.strip()
        driver.get(web)
        navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
        responseStart = driver.execute_script("return window.performance.timing.responseStart")
        domComplete = driver.execute_script("return window.performance.timing.domComplete")
        backendPerformance_calc = (responseStart - navigationStart)/1000
        frontendPerformance_calc = (domComplete - responseStart)/1000
        data = f'{{"server_name":"{server_name}","timestamp":"{hoy}","url":"{web}","t_backend_seg":"{backendPerformance_calc}","t_frontend_seg":"{frontendPerformance_calc}"}}'
        print('opcion B: ' +data)
finally:
    driver.quit()
    display.stop()
