from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from pandas import *
import time


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")


accountData = read_csv("account.csv", dtype=str)
CUIL = accountData["CUIL"].tolist()[0]
PASS = accountData["PASSWORD"].tolist()[0]

companyData = read_csv("company.csv", dtype=str)
COMPANY = companyData["COMPANY"].tolist()[0]


class customer:
    def __init__(self, cuil, condition, amount):
        self.cuil = cuil
        self.condition = condition
        self.amount = amount


customersData = read_csv("clients.csv", dtype=str)
customersCuil = customersData["CUIL"].tolist()
customersCondition = customersData["CONDITION"].tolist()
customersAmount = customersData["AMOUNT"].tolist()

clientsList = []
for index, client in enumerate(customersCuil):
    customerCuil = str(customersCuil[index])
    customerCondition = customersCondition[index]
    customerAmount = customersAmount[index]
    if len(customerCuil) < 5:
        customerCuil = ""
    clientsList.append(customer(customerCuil, customerCondition, customerAmount))


def findElement(path):
    return driver.find_element("xpath", path)


def findElements(path):
    return driver.find_elements("xpath", path)


def findElementAndClick(path):
    element = driver.find_element("xpath", path)
    element.click()
    driver.implicitly_wait(10)
    return


def nextStep():
    nextStep = findElement("//input[@value='Continuar >']")
    nextStep.click()
    time.sleep(0.5)
    return


def logIn():
    accountUsername = findElement("//input[@id='F1:username']")
    accountUsername.send_keys(CUIL)
    findElementAndClick("//input[@id='F1:btnSiguiente']")
    accountPassword = findElement("//input[@id='F1:password']")
    accountPassword.send_keys(PASS)
    findElementAndClick("//input[@id='F1:btnIngresar']")
    findElementAndClick("//input[@value='" + COMPANY + "']")


def generateInvoice(cuil, condition, amount):
    findElementAndClick("//a[@id='btn_gen_cmp']")
    time.sleep(0.9)
    sellPoint = Select(findElement("//select[@id='puntodeventa']"))
    time.sleep(0.9)
    sellPoint.select_by_index("1")
    time.sleep(0.5)
    nextStep()

    concept = Select(findElement("//select[@id='idconcepto']"))
    concept.select_by_index("2")
    findElementAndClick("//input[@id='fsd_btn']")
    currentMonthDaysSince = findElements(
        "//td[contains(@class, 'day') and not(contains(@class, 'othermonth')) and not(contains(@class, 'wn')) and not(contains(@class, 'name'))]"
    )
    currentMonthDaysSince[0].click()
    time.sleep(0.5)
    findElementAndClick("//input[@id='fsh_btn']")
    currentMonthDaysTo = findElements(
        "//td[contains(@class, 'day') and not(contains(@class, 'othermonth')) and not(contains(@class, 'wn')) and not(contains(@class, 'name'))]"
    )
    currentMonthDaysTo[-1].click()
    nextStep()

    conditionIVA = Select(findElement("//select[@id='idivareceptor']"))
    conditionIVA.select_by_index(condition)
    cuilInput = findElement("//input[@id='nrodocreceptor']")
    cuilInput.send_keys(cuil)
    findElementAndClick("//form[@id='formulario']")
    time.sleep(0.5)
    findElementAndClick("//input[@id='formadepago1']")
    nextStep()

    service = findElement("//textarea[@id='detalle_descripcion1']")
    service.send_keys("Servicios Informaticos")
    driver.implicitly_wait(100)
    seleccionUnidad = Select(findElement("//select[@id='detalle_medida1']"))
    seleccionUnidad.select_by_index("7")
    driver.implicitly_wait(100)
    amountInput = findElement("//input[@id='detalle_precio1']")
    amountInput.send_keys(amount)
    nextStep()

    findElementAndClick("//input[@id='btngenerar']")
    time.sleep(0.9)
    driver.switch_to.alert.accept()
    time.sleep(0.9)

    findElementAndClick("//input[@value='Menú Principal']")


driver.get(
    "https://auth.afip.gov.ar/contribuyente_/login.xhtml?action=SYSTEM&system=rcel"
)

logIn()
for client in clientsList:
    generateInvoice(client.cuil, client.condition, client.amount)

input("Press ENTER to exit")
