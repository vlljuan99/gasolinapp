from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time


def scraper(ciudad, direccion):

    chromeoptions = webdriver.ChromeOptions()
    chromeoptions.add_argument('--start-minimized')
    chromeoptions.add_argument('--disable-extensions')

    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=chromeoptions)

    # driver.minimize_window()
    driver.get('https://www.dieselogasolina.com/calcular-ruta.html')

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                           '/html/body/div[2]/div/div[3]/p/button')))\
        .click()

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                           '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/div[1]/input')))\
        .send_keys(ciudad)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                           '/html/body/div[3]')))\
        .click()

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                           '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/div[3]/input')))\
        .send_keys(direccion)

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                           '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/input[2]')))\
        .click()

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                           '/html/body/div[1]/div/div[2]/div/div[3]/div/p[2]/button[1]')))\
        .click()

    WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                           '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div[7]/div/div[4]/div[1]/div[3]/div[2]/p[4]/span')))

    precio_gasolina = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div[7]/div/div[4]/div[1]/div[3]/div[2]/p[4]/span')
    precio_gasolina = precio_gasolina.text

    trayecto_kms = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div[7]/div/div[4]/div[1]/div[1]/p[2]')
    trayecto_kms = trayecto_kms.text

    # DIESEL ---------------------------------------------------
    WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                           '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div[3]/ul/li[3]/label')))\
        .click()

    # time.sleep(2)


    WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                           '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/input[2]')))\
        .click()

    # time.sleep(2)

    WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                           '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div[7]/div/div[4]/div[1]/div[3]/div[2]/p[4]/span')))

    time.sleep(2)

    precio_diesel = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div[7]/div/div[4]/div[1]/div[3]/div[2]/p[4]/span')
    precio_diesel = precio_diesel.text

    precios = {"precio_gasolina": precio_gasolina,
               "precio_diesel": precio_diesel,
               "trayecto_kms": trayecto_kms,}

    return precios
