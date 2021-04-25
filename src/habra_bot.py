import logging
import os
import errno
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from telegram.ext import Updater

CHAT_ID = "-1001468860198"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(token=os.environ.get('BOT_TOKEN'), use_context=True)

chrome_options = Options()

chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)


def silent_remove(filename):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise


def send_message_clean_and_quit(message):
    updater.bot.send_message(chat_id=CHAT_ID, text=message)
    driver.quit()
    updater.stop()


try:
    wait = WebDriverWait(driver, 10)

    driver.get(os.environ.get('TARGET_URL'))

    confirmationCheckBox = wait.until(
        EC.presence_of_element_located((By.XPATH, './/*[@id="condition"]')))

    submitBookingButton = wait.until(EC.presence_of_element_located(
        (By.XPATH, './/*[@id="submit_Booking"]/input[1]')))

    driver.execute_script("arguments[0].click();", confirmationCheckBox)
    driver.execute_script("arguments[0].click();", submitBookingButton)

    confirmationElement = driver.find_element_by_xpath(
        ".//*[contains(text(), 'Veuillez recommencer')]")

    driver.quit()
    updater.stop()
except NoSuchElementException:
    updater.bot.send_message(chat_id=CHAT_ID, text="Harba is ALIVE")

    silent_remove("screenshot.png")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    driver.save_screenshot("screenshot.png")

    updater.bot.send_photo(
        chat_id=CHAT_ID, photo=open('screenshot.png', 'rb'))
except TimeoutException:
    send_message_clean_and_quit(
        "Habra : Loading Error the website maybe down a manual check can be a good idea!!!!")
