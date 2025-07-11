import time
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
USERNAME = os.getenv("IG_USER")
PASSWORD = os.getenv("IG_PASS")

# Typing with random delay per character (human-like)
def human_delay():
    return random.uniform(0.03, 0.1)

def type_like_human(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(human_delay())

# Chrome driver setup (headless=False for debugging locally)
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--start-maximized')
# options.add_argument('--headless')  # Uncomment for headless mode on Render

driver = webdriver.Chrome(options=options)

# Login to Instagram
def login():
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    type_like_human(username_input, USERNAME)
    type_like_human(password_input, PASSWORD)
    password_input.send_keys(Keys.ENTER)
    time.sleep(7)

    # Handle "Not Now"
    try:
        not_now = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
        not_now.click()
        time.sleep(3)
    except:
        pass

# Track last replied messages (to avoid double replies)
last_messages = {}

# Monitor all group chats
def monitor_all_gcs():
    driver.get("https://www.instagram.com/direct/inbox/")
    time.sleep(5)
    
    gcs = driver.find_elements(By.XPATH, "//div[contains(@aria-label,'Conversation')]")
    
    for i in range(min(10, len(gcs))):  # Check top 10 recent threads
        try:
            gcs[i].click()
            time.sleep(3)

            group_name = driver.find_element(By.XPATH, "//h2").text
            messages = driver.find_elements(By.XPATH, "//div[contains(@class,'_a9zs')]/div")
            last_msg = messages[-1].text.strip() if messages else ""
            sender = driver.find_elements(By.XPATH, "//h3")[0].text.split("\n")[0]

            if group_name not in last_messages or last_messages[group_name] != last_msg:
                print(f"💬 New message in '{group_name}' from @{sender}: {last_msg}")
                if USERNAME.lower() not in last_msg.lower():
                    reply_box = driver.find_element(By.TAG_NAME, "textarea")
                    reply_box.click()
                    reply_msg = f"@{sender} TERI GND FAD DUGA 🤣"
                    type_like_human(reply_box, reply_msg)
                    reply_box.send_keys(Keys.ENTER)
                    print(f"✅ Replied to @{sender} in '{group_name}'")
                    last_messages[group_name] = last_msg

            driver.get("https://www.instagram.com/direct/inbox/")
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Error in GC loop: {e}")
            driver.get("https://www.instagram.com/direct/inbox/")
            time.sleep(2)

# Start everything
keep_alive()
login()

while True:
    monitor_all_gcs()
    time.sleep(1)  # Check every second ⚡
