import json
from selenium import webdriver
import time
from send_status import send_telegram
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from interval import every
from datetime import datetime

with open('config.json') as config_file:
    data = json.load(config_file)

chrome_options = Options()

# Next 2 lines prevent selenium detection as a bot
chrome_options.add_argument("--disable-blink-features")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# TODO: Сделать запуск в headless режиме
# chrome_options.headless = True
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('disable-gpu')

service = Service(ChromeDriverManager().install())


def checkprofile():
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = "https://portal-portail.apps.cic.gc.ca/signin?lang=en"

    # driver.minimize_window()
    driver.get(url)

    username = driver.find_element(By.XPATH, '//*[@id="user-control"]')
    login = data["login"]
    username.send_keys(login)

    password_input = driver.find_element(By.XPATH, '//*[@id="password-control"]')
    password = data["password"]
    password_input.send_keys(password)
    time.sleep(3)

    driver.find_element(By.XPATH, '//*[@id="Login.SignInTitle_action_button0"]').click()
    time.sleep(3)

    driver.find_element(By.ID, 'btnIAgree').click()

    time.sleep(3)

    result = driver.find_element(By.XPATH,
                                 '/html/body/ircc-portal-root/common-shell/div/main/ircc-portal-homepage/mat-sidenav-container/mat-sidenav-content/div/div/ng-component/div[2]/div/ircc-portal-paginated-table-component/div/div/div/table/tbody/tr[1]/td[5]/span[2]').text

    if result == 'Submitted':
        print('\33[33m' + datetime.now().strftime(
            '%d-%m-%Y %H:%M:%S') + ' Current status: Nothing new, try again later.' + '\33[0m')

    else:
        driver.get_screenshot_as_file("screenshot.png")
        print('\033[32m' + datetime.now().strftime('%d-%m-%Y %H:%M:%S') + ' Current status: Update!' + '\033[0m')
        send_telegram('Ghost update! Check profile ASAP')

    driver.quit()


checkprofile()

every(data['timer'], checkprofile)