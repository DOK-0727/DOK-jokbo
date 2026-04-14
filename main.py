from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_path = "/Users/handokyung/Desktop/Python/chromedriver-mac-arm64/chromedriver"
service = Service(chrome_path)
driver = webdriver.Chrome(service=service)

url = "https://everytime.kr"
driver.get(url)

wait = WebDriverWait(driver, 15)

def login():
    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.continue"))
    ).click()

    wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "로그인"))
    ).click()

    wait.until(
        EC.presence_of_element_located((By.NAME, "id"))
    ).send_keys("dokyung2727")

    wait.until(
        EC.presence_of_element_located((By.NAME, "password"))
    ).send_keys("201745hksS!")

    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
    ).click()

    wait.until(lambda d: "login" not in d.current_url)

def search():
    search_form = driver.find_element(By.CSS_SELECTOR, "form.search ")
    search_input = search_form.find_element(By.CSS_SELECTOR, "input")

    search_input.send_keys("ㅇㄱㄹ", Keys.ENTER)

login()
search()
time.sleep(5)