from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re


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


def search(subject, professor, short, message):
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

        if ((((subject in title_text or short in title_text) and professor in title_text)
            or
            ((subject in body_text or short in body_text) and professor in body_text))
            and
            (("삽니다" in title_text or "사요" in title_text or "구합니다" in title_text or "구해요" in title_text)
            or
            ("삽니다" in body_text or "사요" in body_text or "구합니다" in body_text or "구해요" in body_text))):
            while True:
                elements = driver.find_elements(By.CSS_SELECTOR, "h2.medium.bold")

                for el in elements:
                    if title_text in el.text:

                        link = el.find_element(By.XPATH, "./ancestor::a")

                        driver.execute_script(
                            "arguments[0].scrollIntoView({block: 'center'});", link
                        )
                        time.sleep(0.5)

                        try:
                                link.click()
                        except:
                            driver.execute_script("arguments[0].click();", link)

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
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='전송']"))
            ).click()

            alert = wait.until(EC.alert_is_present())
            alert.accept()


def response():
    driver.get("https://everytime.kr/message")

    chats = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.item"))
    )

    for i in range(len(chats)):
        wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.modalwrap"))
        )

        chats[i].click()

        texts = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.item"))
        )

        text = texts[len(texts) - 2].text

        content = text.split("글 내용:")[1].split("\n")[0].strip()
        match = re.search(r"(.+?)\((.+?) 교수님\)", content)

        if not match:
            continue

        subject_name = match.group(1).strip()
        professor_name = match.group(2).strip()

        for key, value in subject_dict.items():
            if (
                    value["subject"] == subject_name
                    and value["professor"] == professor_name
            ):
                key, information = subject_list[key - 1]
                message = information["message"]

                all_text = "\n".join([t.text for t in texts])

                if message in all_text:
                    continue

                wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.send"))
                ).click()

                wait.until(
                    EC.element_to_be_clickable((By.NAME, "message"))
                ).send_keys(message)

                wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input.button"))
                ).click()

                alert = wait.until(EC.alert_is_present())
                alert.accept()


subject_dict = {
    1: {
        "subject": "컴퓨터공학개론",
        "short": "컴공개",
        "professor": "ㅇㄱㄹ",
        "message": "컴퓨터공학개론(ㅇㄱㄹ 교수님)\n2025학년도 1학기 중간고사 10,000₩\n2025학년도 1학기 기말고사 10,000₩\n2026학년도 1학기 중간고사 10,000₩\n2025학년도 1학기 중간/기말고사 15,000₩\n\n2025/26학년도 1학기 중간/기말고사 25,000₩\nhttps://open.kakao.com/o/s6DCeCpi\n구매 의향 있으신가요?"
    },
    2: {
        "subject": "C프로그래밍",
        "short": "C프",
        "professor": "ㅇㅂㄱ",
        "message": "C프로그래밍(ㅇㅂㄱ 교수님)\n2024학년도 1학기 중간고사 10,000₩\n2024학년도 1학기 기말고사 10,000₩\n2025학년도 1학기 중간고사 10,000₩\n2025학년도 1학기 기말고사 10,000₩\n\n2024학년도 1학기 중간/기말고사 15,000₩\n2025학년도 1학기 중간/기말고사 15,000₩\n\n2024/25학년도 1학기 중간/기말고사 25,000₩\nhttps://open.kakao.com/o/skE6iuqi\n구매 의향 있으신가요?"
    },
    3: {
        "subject": "대학수학1",
        "short": "대수1",
        "professor": "ㅂㄱㅅ",
        "message": "대학수학1(ㅂㄱㅅ 교수님)\n2023학년도 1학기 중간고사 10,000₩\n2024학년도 1학기 중간고사 10,000₩\n2026학년도 1학기 중간고사 10,000₩\n\n2023/24/26학년도 1학기 중간고사 25,000₩\nhttps://open.kakao.com/o/sx3Ykuqi\n구매 의향 있으신가요?"
    },
    4: {
        "subject": "데이터베이스",
        "short": "데베",
        "professor": "ㅅㅎㅅ",
        "message": "데이터베이스(ㅅㅎㅅ 교수님)\n2024학년도 1학기 중간고사 10,000₩\n2024학년도 1학기 기말고사 10,000₩\n\n2024학년도 1학기 중간/기말고사 15,000₩\nhttps://open.kakao.com/o/sOKzbxqi\n구매 의향 있으신가요?"
    },
    5: {
        "subject": "통일의인문학적이해",
        "short": "통인문",
        "professor": "ㄴㄱㅇ,ㅂㅅㅈ",
        "message": "통일의인문학적이해(ㄴㄱㅇ,ㅂㅅㅈ 교수님)\n2025학년도 2학기 중간고사 10,000₩\n2025학년도 2학기 기말고사 10,000₩\n\n2025학년도 2학기 중간/기말고사 15,000₩\nhttps://open.kakao.com/o/s6iRCDqi\n구매 의향 있으신가요?"
    },
    6: {
        "subject": "기술변화와소비시장융합:자동차와코스메틱",
        "short": "기소융",
        "professor": "ㄱㅅㅇ",
        "message": "기술변화와소비시장융합:자동차와코스메틱(ㄱㅅㅇ 교수님)\n2025학년도 2학기 중간/기말고사 15,000₩\nhttps://open.kakao.com/o/sG2hDDqi\n구매 의향 있으신가요?"
    },
    7: {
        "subject": "경영학원론",
        "short": "경원론",
        "professor": "ㄱㄱㅅ",
        "message": "경영학원론(ㄱㄱㅅ 교수님)\n2025학년도 2학기 중간고사 10,000₩\n2025학년도 2학기 기말고사 10,000₩\n\n2025학년도 2학기 중간/기말고사 15,000₩\n\n2024/25학년도 2학기 중간/기말고사 20,000₩\nhttps://open.kakao.com/o/sPNTREqi\n구매 의향 있으신가요?"
    },
    8: {
        "subject": "경영학원론",
        "short": "경원론",
        "professor": "ㄱㅊㅇ",
        "message": "경영학원론(ㄱㅊㅇ 교수님)\n2025학년도 1학기 중간고사 10,000₩\n2025학년도 1학기 기말고사 10,000₩\n\n2025학년도 1학기 중간/기말고사 15,000₩\n\n2024/25학년도 1학기 중간/기말고사 20,000₩\nhttps://open.kakao.com/o/skkcSEqi\n구매 의향 있으신가요?"
    },
    9: {
        "subject": "컴퓨팅적사고",
        "short": "컴사",
        "professor": "ㅇㅁㅈ",
        "message": "컴퓨팅적사고(ㅇㅁㅈ 교수님))\n2024학년도 1학기 중간고사 10,000₩\nhttps://open.kakao.com/o/smTxjuqi\n구매 의향 있으신가요?"
    },
    10: {
        "subject": "C프로그래밍",
        "short": "C프",
        "professor": "ㅂㅅㅇ",
        "message": "C프로그래밍(ㅂㅅㅇ 교수님)\n2021학년도 1학기 중간고사 10,000₩\nhttps://open.kakao.com/o/suL4dfri\n구매 의향 있으신가요?"
    },
    11: {
        "subject": "대학물리학1",
        "short": "대물1",
        "professor": "ㄱㅊㅁ",
        "message": "대학물리학1(ㄱㅊㅁ 교수님)\n2024학년도 1학기 중간고사 10,000₩\n2024학년도 1학기 기말고사 10,000₩\n\n2024학년도 1학기 중간/기말고사 15,000₩\nhttps://open.kakao.com/o/sfER7eri\n구매 의향 있으신가요?"
    },
    12: {
        "subject": "공학수학1",
        "short": "공수1",
        "professor": "ㅇㄱㅅ",
        "message": "공학수학1(ㅇㄱㅅ 교수님)\n2024학년도 1학기 중간고사 5,000₩\n2024학년도 1학기 기말고사 5,000₩\n\n2024학년도 1학기 중간/기말고사 75,000₩\nhttps://open.kakao.com/o/s8PvShri\n구매 의향 있으신가요?"
    },
    13: {
        "subject": "펜데믹이후의공공철학",
        "short": "펜이공철",
        "professor": "ㄱㅎㅅ",
        "message": "펜데믹이후의공공철학(ㄱㅎㅅ 교수님)\n2024학년도 2학기 중간고사 10,000₩\nhttps://open.kakao.com/o/spS70kri\n구매 의향 있으신가요?"
    },
    14: {
        "subject": "현대사회와지속가능경영",
        "short": "현사지경",
        "professor": "ㅇㅈㅇ",
        "message": "현대사회와지속가능경영(ㅇㅈㅇ 교수님)\n2025학년도 2학기 중간고사 10,000₩\n2025학년도 2학기 기말고사 10,000₩\n\n2025학년도 2학기 중간/기말고사 15,000₩\nhttps://open.kakao.com/o/snyH7kri\n구매 의향 있으신가요?"
    }
}

function = {
    "작성": lambda: write(subject, professor, short),
    "검색": lambda: [ search(v["subject"], v["professor"], v["short"], v["message"]) for v in subject_dict.values() ],
    "답장": lambda: response()
}

function_list = list(function.items())

for idx, function_name in enumerate(function.keys(), start=1):
    print(idx, function_name)

function_number = list(map(int, input("번호를 입력해주세요:").replace(",", " ").split()))

subject_list = [(v["subject"], v) for v in subject_dict.values()]

if (function_number == [1]):
    for index, (subject, information) in enumerate(subject_list, start=1):
        print(index, subject, information["short"], information["professor"])

    subject_number = int(input("번호를 입력해주세요:"))

    subject, information = subject_list[subject_number - 1]
    short = information["short"]
    professor = information["professor"]
    message = information["message"]

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
