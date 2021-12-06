import json
import gzip
import argparse
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from rich.console import Console
import rich.traceback

import time 

console = Console()
console.clear()
rich.traceback.install()


parser = argparse.ArgumentParser(description="Opis:")
parser.add_argument('file', help = "Użytkowniku podaj nazwę pliku do zapisu")
args = parser.parse_args()

option = Options()
option.add_argument('--disable-notifications')

service = Service('chromedriver.exe')
driver = webdriver.Chrome(service = service, options = option)

driver.get('https://siatka.org/tagi/luk-politechnika-lublin/')

button = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cn-accept-cookie"]')))
button.click()

button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cookieNoticeContent"]/table/tbody/tr/td/button')))
button.click()

lista = []

for index in range(1,15):
    elements = driver.find_elements(By.CLASS_NAME, 'entry-content [href]')

    for element in elements:
        lista.append(element.get_attribute('href'))

    driver.get(f'https://siatka.org/tagi/luk-politechnika-lublin/page{index + 1}')

driver.close()

with gzip.open(args.file + '.json.gzip', 'wt', encoding = 'utf-8') as f:
    json.dump(lista, f)

with gzip.open(args.file + '.json.gzip', 'rt', encoding = 'utf-8') as f:
    y = json.load(f)
    console.print(y)