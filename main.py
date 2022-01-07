import json
from selenium import webdriver
import time
from send_status import send_telegram
from selenium.webdriver.chrome.options import Options
from interval import every
from datetime import datetime

with open('config.json') as config_file:
    data = json.load(config_file)

PATH = r"C:\Users\_Lucas_\Downloads\chromedriver.exe"
chrome_options = Options()


# TODO: Сделать запуск в headless режиме
# chrome_options.headless = True
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('disable-gpu')


def checkprofile():
    driver = webdriver.Chrome(PATH, options=chrome_options)
    url = "https://onlineservices-servicesenligne-cic.fjgc-gccf.gc.ca/mycic/gccf?lang=eng&idp=gckey&svc=/mycic/start"

    def buttonclick():
        driver.find_element_by_class_name('btn.btn-primary').click()
        time.sleep(1)

    driver.minimize_window()
    driver.get(url)

    username = driver.find_element_by_id('token1')
    login = data["login"]
    username.send_keys(login)

    password_input = driver.find_element_by_id('token2')
    password = data["password"]
    password_input.send_keys(password)
    time.sleep(2)

    buttonclick()
    buttonclick()
    buttonclick()

    answer = driver.find_element_by_id('answer')

    questions = data['questions_and_answers']

    for key, value in questions.items():
        if key in driver.page_source:
            answer.send_keys(value)
            buttonclick()

    result = driver.find_element_by_xpath('/html/body/div[1]/main/div[1]/div/table/tbody/tr[1]/td[6]').text

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
