from selenium import webdriver
import time
from config import username_token, password_token, question_one, answer_one, question_two, answer_two, question_three, \
    answer_three, question_four, answer_four
from send_status import send_telegram

PATH = r"C:\Users\_Lucas_\Downloads\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://onlineservices-servicesenligne-cic.fjgc-gccf.gc.ca/mycic/gccf?lang=eng&idp=gckey&svc=/mycic/start")

username = driver.find_element_by_id('token1')
username.send_keys(username_token)

password = driver.find_element_by_id('token2')
password.send_keys(password_token)
time.sleep(1)


def buttonClick():
    signIN = driver.find_element_by_class_name('btn.btn-primary')
    signIN.click()
    time.sleep(1)


buttonClick()
buttonClick()
buttonClick()

answer = driver.find_element_by_id('answer')

if question_one in driver.page_source:
    answer.send_keys(answer_one)
    buttonClick()

elif question_two in driver.page_source:
    answer.send_keys(answer_two)
    buttonClick()

elif question_three in driver.page_source:
    answer.send_keys(answer_three)
    buttonClick()

elif question_four in driver.page_source:
    answer.send_keys(answer_four)
    buttonClick()

result = driver.find_element_by_xpath('/html/body/div[1]/main/div[1]/div/table/tbody/tr[1]/td[6]').text

if result == 'Read':
    print('Current status' + ': ' + 'Nothing new, try again later.')

else:
    print('Current status' + ': ' + 'Update!')
    send_telegram('Ghost update! Check profile ASAP')

time.sleep(10)
driver.quit()
