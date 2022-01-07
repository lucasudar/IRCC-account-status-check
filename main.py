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

# TODO: Сделать запуск в headless режиме
# chrome_options.headless = True
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('disable-gpu')
# chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"')


def checkprofile():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = "https://onlineservices-servicesenligne-cic.fjgc-gccf.gc.ca/mycic/gccf?lang=eng&idp=gckey&svc=/mycic/start"

    def buttonclick():
        driver.find_element(By.CLASS_NAME, 'btn.btn-primary').click()
        time.sleep(1)

    driver.minimize_window()
    driver.get(url)

    username = driver.find_element(By.ID, 'token1')
    login = data["login"]
    username.send_keys(login)

    password_input = driver.find_element(By.ID, 'token2')
    password = data["password"]
    password_input.send_keys(password)
    time.sleep(2)

    buttonclick()
    buttonclick()
    buttonclick()

    answer = driver.find_element(By.ID, 'answer')

    questions = data['questions_and_answers']

    for key, value in questions.items():
        if key in driver.page_source:
            answer.send_keys(value)
            buttonclick()

    result = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[1]/div/table/tbody/tr[1]/td[6]').text

    if result == 'Read':
        print('\33[33m' + datetime.now().strftime(
            '%d-%m-%Y %H:%M:%S') + ' Current status: Nothing new, try again later.' + '\33[0m')

    else:
        driver.get_screenshot_as_file("screenshot.png")
        print('\033[32m' + datetime.now().strftime('%d-%m-%Y %H:%M:%S') + ' Current status: Update!' + '\033[0m')
        send_telegram('Ghost update! Check profile ASAP')

    driver.quit()

    
checkprofile()

every(data['timer'], checkprofile)
