from selenium import webdriver
import time
from config import username_token, password_token, question_one, answer_one, question_two, answer_two, question_three, \
    answer_three, question_four, answer_four
from send_status import send_telegram
from selenium.webdriver.chrome.options import Options

PATH = r"C:\Users\_Lucas_\Downloads\chromedriver.exe"
chrome_options = Options()
# TODO: Сделать запуск в headless режиме
# chrome_options.headless = True
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('disable-gpu')

driver = webdriver.Chrome(PATH, options=chrome_options)


def buttonclick():
    driver.find_element_by_class_name('btn.btn-primary').click()
    time.sleep(1)


driver.minimize_window()

driver.get("https://onlineservices-servicesenligne-cic.fjgc-gccf.gc.ca/mycic/gccf?lang=eng&idp=gckey&svc=/mycic/start")

username = driver.find_element_by_id('token1')
username.send_keys(username_token)

password = driver.find_element_by_id('token2')
password.send_keys(password_token)
time.sleep(2)

buttonclick()
buttonclick()
buttonclick()

answer = driver.find_element_by_id('answer')

if question_one in driver.page_source:
    answer.send_keys(answer_one)
    buttonclick()

elif question_two in driver.page_source:
    answer.send_keys(answer_two)
    buttonclick()

elif question_three in driver.page_source:
    answer.send_keys(answer_three)
    buttonclick()

elif question_four in driver.page_source:
    answer.send_keys(answer_four)
    buttonclick()

result = driver.find_element_by_xpath('/html/body/div[1]/main/div[1]/div/table/tbody/tr[1]/td[6]').text

if result == 'Read':
    print('\33[33m' + 'Current status: Nothing new, try again later.' + '\33[0m')

else:
    print('\033[32m' + 'Current status: Update!' + '\033[0m')
    send_telegram('Ghost update! Check profile ASAP')

driver.quit()

# TODO: Сделать запуск по интервалу времени