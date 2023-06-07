#!/usr/bin/python3
'''
Medicion de tiempos de respuesta Web
utilizando Selenium.

Descripcion del flujo de medicion:
navigationStart -> redirectStart -> redirectEnd -> fetchStart -> domainLookupStart -> domainLookupEnd
-> connectStart -> connectEnd -> requestStart -> responseStart -> responseEnd
-> domLoading -> domInteractive -> domContentLoaded -> domComplete -> loadEventStart -> loadEventEnd
'''

from random import randint
from time import sleep
from datetime import datetime
from selenium import webdriver
from pyvirtualdisplay import Display
import socket

hoy = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
server_name = socket.gethostname()

display = Display(visible=0, size=(1600, 1200))
display.start()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')

# version script ejecutado en ontenedor
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)

# version de Chromium remota (sin probar aun)
#driver = webdriver.Remote( command.executor='http://localhost:4444/web/hub', desired_capabilities=DesiredCapabilities.CHROME)

sleep(randint(5,30))

try:
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
            print(data)
        
except Exception as e:
    print(f'Error: {e}')

finally:
    driver.quit()
    display.stop()