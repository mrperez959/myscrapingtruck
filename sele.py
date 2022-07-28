import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from vonage import *
import time


DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://id.centraldispatch.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3Dcentraldispatch_authentication%26scope%3Dlisting_service%2520offline_access%2520openid%26response_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Fwww.centraldispatch.com%252Fprotected')

user = "crbtech2"
clave = "Crbrr04$"



viajesdictionary = [""]
pickup = ""
delivery = ""
numvehicles = ""
telefon = ""
cantCarreras = 0
client = vonage.Client(key="417654f5", secret="SmFh6U9kkIkv8jyD")
sms = vonage.Sms(client)
message = ""
smsmio=""
flag = False
driver.find_element(By.ID, 'Username').send_keys(user)
driver.find_element(By.ID, 'password').send_keys(clave)
driver.find_element(By.ID, 'loginButton').click()

driver.get('https://www.centraldispatch.com/protected/listing-search?bypassRedirect=true')
# Origin Form
driver.find_element(By.ID, 'originCityTypeSelector').click()
driver.find_element(By.ID, 'originState').send_keys("GA")
driver.find_element(By.ID, 'originCity').send_keys("Atlanta")
driver.find_element(By.ID, 'originRadius').send_keys("50")

# Destination Form
driver.find_element(By.ID, 'destinationCityTypeSelector').click()
driver.find_element(By.ID, 'destinationState').send_keys('FL')
driver.find_element(By.ID, 'destinationCity').send_keys("Miami")
driver.find_element(By.ID, 'destinationRadius').send_keys("50")

# Minimo de veiculos
driver.find_element(By.ID, 'minVehicles').send_keys("2")
# Estado de los veiculos
driver.find_element(By.ID, 'running').send_keys("Running")
# driver.find_element(By.ID, 'running').send_keys("Non-Running")
driver.find_element(By.ID, 'btnSearch').click()


time.sleep(3.5)
# Hay 4 tr q vinene por de fecto 2 al inicio y 2 al final se recorre a partir de la posicion 2


# A partir de aqui se refresca el codigo
while (True):
    try:
        carreras = driver.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
        print(len(carreras))
        for x in carreras:
            a =carreras[0].find_elements(By.TAG_NAME, 'a')
            pickup = a[0].get_attribute("text")
            delivery = a[1].get_attribute("text")
            numvehicles = a[3].get_attribute("text")
            telefon = a[6].get_attribute("text")
            message = pickup + " -- " + delivery + " -- " + numvehicles + " -- " + telefon
                
            if message not in viajesdictionary or cantCarreras == 0:
                viajesdictionary[cantCarreras] = message
                cantCarreras = cantCarreras+1
                flag = True


        if (flag):
            smsmio = f"In this moment the site has {str(cantCarreras)} new orders : \n"
            
            for viaje in viajesdictionary:
                smsmio = smsmio + viaje + "\n"

            responseData = sms.send_message(
                {
                    "from": "18334391809",
                    "to": "13057754492",
                    "text": str(smsmio),
                }
            )

            if responseData["messages"][0]["status"] == "0":
                print("Message sent successfully.")
                flag = False
            else:
                print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

    except:
        print("Nada Nuevo")
    driver.refresh()
    time.sleep(10)
