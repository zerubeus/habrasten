import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from telegram.ext import Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def check_envs():
    if not os.environ.get('BOT_TOKEN') or not os.environ.get('TARGET_URL'):
        raise Exception('Missing env vars')


def send_message_clean_and_quit(message):
    updater.bot.send_message(chat_id='-1001468860198', text=message)
    driver.quit()
    updater.stop()


try:
    # The bot token
    updater = Updater(token=os.environ.get('BOT_TOKEN'), use_context=True)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    wait = WebDriverWait(driver, 10)

    driver.get(os.environ.get('TARGET_URL'))
    confirmationCheckBox = wait.until(EC.presence_of_element_located((By.XPATH, './/*[@id="condition"]')))
    submitBookingButton = wait.until(EC.presence_of_element_located((By.XPATH, './/*[@id="submit_Booking"]/input[1]')))

    driver.execute_script("arguments[0].click();", confirmationCheckBox)
    driver.execute_script("arguments[0].click();", submitBookingButton)

    confirmationElement = driver.find_element_by_xpath(".//*[contains(text(), 'Veuillez recommencer ultérieurement')]")
    send_message_clean_and_quit("There's no habra for the moment")
except Exception as error:
    print('Habra missing env vars : ', repr(error))
except NoSuchElementException:
    send_message_clean_and_quit("Habra is ALIVE")
except TimeoutException:
    send_message_clean_and_quit("Habra : Loading Error the website maybe down a manual check can be a good idea!!!!")