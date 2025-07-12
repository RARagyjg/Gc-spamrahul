import time
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from keep_alive import keep_alive

# ✅ Hardcoded Session ID (Paste yours here directly)
SESSIONID = "75769536828:f5BHWSqgKAtUbX:1:AYfIcUbKHGapGJmkoPJXHWYCnAWI0xgCRs5xiJ1tqg"

# Start Flask web server for Render
keep_alive()

# Chrome browser setup (headless + humanized)
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('--headless=new')
options.add_argument(f"--user-data-dir=/tmp/profile_{random.randint(1000,9999)}")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/114.0.0.0 Safari/537.36")

# Launch Chrome
driver = webdriver.Chrome(options=options)

# Simulate human typing
def type_like_human(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.03, 0.08))

# Login using session cookie (no detection)
def login_with_cookie():
    driver.get("https://www.instagram.com/")
    driver.add_cookie({"name": "sessionid", "value": SESSIONID})
    time.sleep(2)
    driver.get("https://www.instagram.com/direct/inbox/")
    time.sleep(6)
    print("✅ Logged in using session cookie")

# Track last messages
last_messages = {}

# Monitor and auto reply to all group chats
def monitor_all_gcs():
    driver.get("https://www.instagram.com/direct/inbox/")
    time.sleep(6)

    gcs = driver.find_elements(By.XPATH, "//div[contains(@aria-label,'Conversation')]")

    for i in range(min(10, len(gcs))):
        try:
            gcs[i].click()
            time.sleep(5)

            group_name = driver.find_element(By.XPATH, "//h2").text
            messages = driver.find_elements(By.XPATH, "//div[contains(@class,'_a9zs')]/div")
            last_msg = messages[-1].text.strip() if messages else ""
            sender = driver.find_elements(By.XPATH, "//h3")[0].text.split("\n")[0]

            print(f"📨 Group: {group_name} | Last: {last_msg}")

            if group_name not in last_messages or last_messages[group_name] != last_msg:
                input_box = driver.find_element(By.TAG_NAME, "textarea")
                input_box.click()
                reply_msg = f"@{sender} TERI GND FAD DUGA 🤣"
                type_like_human(input_box, reply_msg)
                input_box.send_keys(Keys.ENTER)
                print(f"✅ Replied to @{sender} in '{group_name}'")
                last_messages[group_name] = last_msg

            driver.get("https://www.instagram.com/direct/inbox/")
            time.sleep(2)

        except Exception as e:
            print(f"⚠️ Error: {e}")
            driver.get("https://www.instagram.com/direct/inbox/")
            time.sleep(2)

# Start bot
login_with_cookie()
while True:
    monitor_all_gcs()
    time.sleep(1)
