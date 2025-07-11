import time
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from keep_alive import keep_alive

# Load .env
load_dotenv()
USERNAME = os.getenv("IG_USER")
PASSWORD = os.getenv("IG_PASS")

# Start 24/7 server (Render requirement)
keep_alive()

# Chrome options for headless + Render fix
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('--headless=new')  # ✅ Use new headless mode
options.add_argument(f"--user-data-dir=/tmp/profile_{random.randint(1000,9999)}")  # ✅ Fix session error

# Launch browser
driver = webdriver.Chrome(options=options)

# Human typing style
def type_like_human(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.03, 0.08))

# Login to Instagram
def login():
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)
    driver.find_element(By.NAME, "username").send_keys(USERNAME)
    password_input = driver.find_element(By.NAME, "password")
    type_like_human(password_input, PASSWORD)
    password_input.send_keys(Keys.ENTER)
    time.sleep(7)

    # Skip Save Login
    try:
        driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]").click()
        time.sleep(3)
    except:
        pass

    # Skip Turn on Notifications
    try:
        driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]").click()
        time.sleep(3)
    except:
        pass

# Track last messages replied to
last_messages = {}

# Monitor all group chats
def monitor_all_gcs():
    driver.get("https://www.instagram.com/direct/inbox/")
    time.sleep(5)

    gcs = driver.find_elements(By.XPATH, "//div[contains(@aria-label,'Conversation')]")

    for i in range(min(10, len(gcs))):  # Check top 10 threads
        try:
            gcs[i].click()
            time.sleep(3)

            group_name = driver.find_element(By.XPATH, "//h2").text
            messages = driver.find_elements(By.XPATH, "//div[contains(@class,'_a9zs')]/div")
            last_msg = messages[-1].text.strip() if messages else ""
            sender = driver.find_elements(By.XPATH, "//h3")[0].text.split("\n")[0]

            if group_name not in last_messages or last_messages[group_name] != last_msg:
                if USERNAME.lower() not in last_msg.lower():
                    input_box = driver.find_element(By.TAG_NAME, "textarea")
                    input_box.click()
                    reply_msg = f"@{sender} TERI GND FAD DUGA 🤣"
                    type_like_human(input_box, reply_msg)
                    input_box.send_keys(Keys.ENTER)
                    print(f"✅ Replied to @{sender} in '{group_name}'")
                    last_messages[group_name] = last_msg

            driver.get("https://www.instagram.com/direct/inbox/")
            time.sleep(1)

        except Exception as e:
            print(f"⚠️ Error: {e}")
            driver.get("https://www.instagram.com/direct/inbox/")
            time.sleep(1)

# Start bot
login()
while True:
    monitor_all_gcs()
    time.sleep(1)
