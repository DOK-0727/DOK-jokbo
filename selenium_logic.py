from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import re


def login(user_id, user_pw):
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.continue"))).click()

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "로그인"))).click()

    wait.until(EC.presence_of_element_located((By.NAME, "id"))).send_keys(user_id)
    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(user_pw)

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))).click()

    try:
        alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
        print("로그인 실패:", alert.text)
        alert.accept()
        raise Exception("로그인 실패")
    except TimeoutException:
        pass

    wait.until(lambda d: "login" not in d.current_url)


def write(subject, professor, short):
    driver.get("https://everytime.kr/370471")

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "새 글을 작성해주세요!"))).click()

    wait.until(EC.presence_of_element_located((By.NAME, "title"))) \
        .send_keys(f"{subject} ({professor} 교수님) 족보 있습니다")

    wait.until(EC.presence_of_element_located((By.NAME, "text"))) \
        .send_keys(f"{subject},{short} ({professor} 교수님) 족보 있습니다. 쪽지주세요.")

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.anonym"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.submit"))).click()

    alert = wait.until(EC.alert_is_present())
    alert.accept()


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

                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
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

            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.messagesend"))).click()

            wait.until(EC.presence_of_element_located((By.NAME, "message"))).send_keys(message)

            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='전송']"))).click()

            alert = wait.until(EC.alert_is_present())
            alert.accept()


def response(subjects):
    driver.get("https://everytime.kr/message")

    chats = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.item"))
    )

    for i in range(len(chats)):
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.modalwrap")))

        chats[i].click()

        texts = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.item"))
        )

        text = texts[len(texts) - 2].text

        if "글 내용:" not in text:
            continue

        content = text.split("글 내용:")[1].split("\n")[0].strip()
        match = re.search(r"(.+?)\((.+?) 교수님\)", content)

        if not match:
            continue

        subject_name = match.group(1).strip()
        professor_name = match.group(2).strip()

        for v in subjects:
            if (
                    v["subject"] == subject_name and
                    v["professor"] == professor_name
            ):
                all_text = "\n".join([t.text for t in texts])

                if v["message"] in all_text:
                    continue

                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.send"))).click()

                wait.until(EC.presence_of_element_located((By.NAME, "message"))) \
                    .send_keys(v["message"])

                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.button"))).click()

                alert = wait.until(EC.alert_is_present())
                alert.accept()


def run_bot(user_id, user_pw, function_number, subject_number, subjects):
    chrome_path = "/Users/handokyung/Desktop/DOK/Python/chromedriver-mac-arm64/chromedriver"
    service = Service(chrome_path)

    global driver, wait
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 15)

    driver.get("https://everytime.kr/")

    # login(user_id, user_pw)

    if 1 in function_number:
        if subject_number == 0:
            for v in subjects:
                write(v["subject"], v["professor"], v["short"])
        else:
            subject = subjects[subject_number - 1]
            write(subject["subject"], subject["professor"], subject["short"])

    if 2 in function_number:
        if subject_number == 0:
            for v in subjects:
                search(v["subject"], v["professor"], v["short"], v["message"])
        else:
            subject = subjects[subject_number - 1]
            search(subject["subject"], subject["professor"], subject["short"], subject["message"])

    if 3 in function_number:
        response(subjects)

    driver.quit()
