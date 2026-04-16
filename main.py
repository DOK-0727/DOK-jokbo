from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


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


def write(subject, professor, short):
    driver.get("https://everytime.kr/370471")

    wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "새 글을 작성해주세요!"))
    ).click()

    wait.until(
        EC.presence_of_element_located((By.NAME, "title"))
    ).send_keys(f"{subject} ({professor} 교수님) 족보 있습니다")

    wait.until(
        EC.presence_of_element_located((By.NAME, "text"))
    ).send_keys(f"{subject},{short} ({professor} 교수님) 족보 있습니다. 쪽지주세요.")

    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "li.anonym"))
    ).click()

    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "li.submit"))
    ).click()


def search(subject, professor, short):
    driver.get("https://everytime.kr/370471")

    titles = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2.medium.bold"))
    )

    texts = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.medium"))
    )

    for i in range(len(titles)):
        title_text = titles[i].text
        body_text = texts[i].text

        if (subject or short) in title_text or professor in title_text \
                or (subject or short) in body_text or professor in body_text:
            print("\n")
            print("제목:", title_text)
            print("본문:", body_text)
            print("\n")


def letter(title, message):
    driver.get("https://everytime.kr/370471")

    while True:
        elements = driver.find_elements(By.CSS_SELECTOR, "h2.medium.bold")

        for el in elements:
            if title in el.text:
                el.find_element(By.XPATH, "./ancestor::a").click()
                break
        else:
            last_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if last_height == new_height:
                print("글을 발견하지 못했습니다")
                return
            continue

        break

    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "li.messagesend"))
    ).click()

    wait.until(
        EC.presence_of_element_located((By.NAME, "message"))
    ).send_keys(message)

    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.button"))
    ).click()

subject = {
    "컴퓨터공학개론": {
        "short": "컴공개",
        "professor": "ㅇㄱㄹ",
        "message": "컴퓨터공학개론(ㅇㄱㄹ 교수님)\n2025학년도 1학기 중간고사 10,000₩\n2025학년도 1학기 기말고사 10,000₩\n\n2025학년도 1학기 중간/기말고사 15,000₩\nhttps://open.kakao.com/o/s6DCeCpi"
    },
    "C프로그래밍": {
        "short": "C프",
        "professor": "ㅇㅂㄱ",
        "message": "C프로그래밍(ㅇㅂㄱ 교수님)\n2024학년도 1학기 중간고사 10,000₩\n2024학년도 1학기 기말고사 10,000₩\n2025학년도 1학기 중간고사 10,000₩\n2025학년도 1학기 기말고사 10,000₩\n\n2024학년도 1학기 중간/기말고사 15,000₩\n2025학년도 1학기 중간/기말고사 15,000₩\n\n2024/25학년도 1학기 중간/기말고사 25,000₩\nhttps://open.kakao.com/o/skE6iuqi"
    },
    "대학수학1": {
        "short": "대수1",
        "professor": "ㅂㄱㅅ",
        "message": "대학수학1(ㅂㄱㅅ 교수님)\n2024학년도 1학기 중간고사 10,000₩\nhttps://open.kakao.com/o/sx3Ykuqi"
    },
    "데이터베이스": {
        "short": "데베",
        "professor": "ㅅㅎㅅ",
        "message": "데이터베이스(ㅅㅎㅅ 교수님)\n2024학년도 1학기 중간고사 10,000₩\n2024학년도 1학기 기말고사 10,000₩\n\n2024학년도 1학기 중간/기말고사 15,000₩\nhttps://open.kakao.com/o/sOKzbxqi"
    },
    "통일의인문학적이해": {
        "short": "통인문",
        "professor": "ㄴㄱㅇ,ㅂㅅㅈ",
        "message": "통일의인문학적이해(ㄴㄱㅇ,ㅂㅅㅈ 교수님)\n2025학년도 2학기 중간고사 10,000₩\n2025학년도 2학기 기말고사 10,000₩\n\n2025학년도 2학기 중간/기말고사 15,000₩\nhttps://open.kakao.com/o/s6iRCDqi"
    },
    "기술변화와소비시장융합:자동차와코스메틱": {
        "short": "기소융",
        "professor": "ㄱㅅㅇ",
        "message": "기술변화와소비시장융합:자동차와코스메틱(ㄱㅅㅇ 교수님)\n2025학년도 2학기 중간/기말고사 15,000₩\nhttps://open.kakao.com/o/sG2hDDqi"
    }
}

function = {
    "작성": lambda: write(subject_name, professor, short),
    "검색": lambda: search(subject_name, professor, short),
    "쪽지": lambda: letter(title, message)
}

subject_list = list(subject.items())

for index, (subject, information) in enumerate(subject_list, start=1):
    print(index, subject, information["short"], information["professor"])

subject_number = int(input("번호를 입력해주세요:"))

subject_name, information = subject_list[subject_number - 1]
short = information["short"]
professor = information["professor"]
message = information["message"]

function_list = list(function.items())

for idx, function_name in enumerate(function.keys(), start=1):
    print(idx, function_name)

function_number = list(map(int, input("번호를 입력해주세요:").replace(",", " ").split()))

if (function_number == [3]):
    title = input("글의 제목을 입력해주세요:")

chrome_path = "/Users/handokyung/Desktop/Python/chromedriver-mac-arm64/chromedriver"
service = Service(chrome_path)
driver = webdriver.Chrome(service=service)

driver.get("https://everytime.kr")
wait = WebDriverWait(driver, 15)

login()
time.sleep(2)
for n in function_number:
    function_list[n - 1][1]()
    time.sleep(2)
