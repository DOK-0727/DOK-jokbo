from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ==============================
# 과목 데이터
# ==============================
jokbo = {
    "컴퓨터공학개론": "ㅇㄱㄹ",
    "C프로그래밍": "ㅇㅂㄱ",
    "데이터베이스": "ㅅㅎㅅ"
}

jokbo_list = list(jokbo.items())

for idx, (subject, professor) in enumerate(jokbo_list, start=1):
    print(idx, subject, professor)

n = int(input("번호를 입력해주세요:"))

chrome_path = "/Users/handokyung/Desktop/Python/chromedriver-mac-arm64/chromedriver"
service = Service(chrome_path)
driver = webdriver.Chrome(service=service)

driver.get("https://everytime.kr")
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

def write(subject, professor):
    driver.get("https://everytime.kr/370471")

    wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "새 글을 작성해주세요!"))
    ).click()

    wait.until(
        EC.presence_of_element_located((By.NAME, "title"))
    ).send_keys(f"{subject} ({professor} 교수님) 족보 있습니다")

    wait.until(
        EC.presence_of_element_located((By.NAME, "text"))
    ).send_keys(f"{subject} ({professor} 교수님) 족보 있습니다. 쪽지주세요.")

    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "li.anonym"))
    ).click()

    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "li.submit"))
    ).click()

def search():
    titles = driver.find_elements(By.CSS_SELECTOR, "h2.medium bold")
    texts = driver.find_elements(By.CSS_SELECTOR, "p.medium bold")

login()
time.sleep(3)
subject, professor = jokbo_list[n-1]
write(subject, professor)
time.sleep(5)