from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


def get_data():
    with open("info.json", mode="r", encoding="utf-8") as data:
        account_data = json.load(data)

    return account_data['email'], account_data['password']


def login(email: str, passowrd: str):
    # Set up the Selenium Chrome driver (use ChromeDriverManager for easier setup)
    options = webdriver.ChromeOptions()

    options.page_load_strategy = 'normal'
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    # Access the webpage
    driver.get('https://www.ea.com/ea-sports-fc/ultimate-team/web-app')
    driver.implicitly_wait(10)
    wait = WebDriverWait(driver, timeout=10)
    try:
        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#Login > div > div > button.btn-standard.call-to-action'))
        ).click()
    except Exception as e:
        print(e)

    # Wait for the page to load fully (adjust time as needed)
    driver.implicitly_wait(10)

    email_selector = '#email'
    password_selector = '#password'

    try:
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, email_selector))
        ).send_keys(email)

        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, password_selector))
        ).send_keys(passowrd)

        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#logInBtn'))
        ).click()

    except Exception as e:
        print(e)
    # Wait until the page is fully loaded
    wait.until(lambda d: d.execute_script(
        'return document.readyState') == 'complete')

    local_storage = driver.execute_script("return window.localStorage;")

    # Pretty-print the local storage data

    cookies = driver.get_cookies()

    with open('session_data.json', mode="w", encoding="utf-8") as session_data:

        # Write local storage as JSON
        json.dump({"local_storage": local_storage}, session_data, indent=4)

        # Add a newline for separation between sections (optional)
        session_data.write("\n")

        # Write cookies as JSON
        json.dump({"cookies": cookies}, session_data, indent=4)

        # Print values to the console for debug purposes
        for key, value in local_storage.items():
            print(f"{key}: {value}")

        for cookie in cookies:
            print(cookie)

    driver.implicitly_wait(10)

    # Close the driver
    driver.quit()


if '__main__':
    email, password = get_data()
    login(email, password)
