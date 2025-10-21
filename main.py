from keep_alive import keep_alive
from instagrapi import Client
import time
import random
import uuid
import itertools

# 🔄 Start keep-alive for Render/Replit
keep_alive()

# 🔐 Login with session ID
cl = Client()
cl.login_by_sessionid("77802598284%3A38M5A0SzWLcqvw%3A4%3AAYh6yiKD0u0La8-wTM9or8oEUlyPtirD7zhGa63XoQ")

# 💬 Message templates (unchanged)
reply_templates = [
    ("OMA  L9 PE_____// " * 20).strip(),
    ("BHAG MATT____////// " * 20).strip(),
    ("TERYY GND FADU BACHE ______/// " * 18).strip(),
    ("CHAL DUMM LAGA HAHAHAAH __///// " * 18).strip()
]

# 🔁 Cycle for rotating messages
msg_cycle = itertools.cycle(reply_templates)

# 🧠 Always pick the latest (top) group chat
def get_gc_thread_id():
    threads = cl.direct_threads(amount=5)
    for thread in threads:
        if thread.is_group:
            return thread.id
    return None

# ✨ Char-by-char simulate function (just delay logic)
def simulate_typing_effect(message):
    simulated = ""
    for char in message:
        simulated += char
        time.sleep(random.uniform(0.01, 0.04))  # Typing effect
    return simulated

# 🚀 Start spamming with typing effect
def start_gc_autospam():
    while True:
        gc_thread_id = get_gc_thread_id()
        if not gc_thread_id:
            print("❌ Group chat not found.")
            time.sleep(30)
            continue

        try:
            msg_base = next(msg_cycle)
            unique_msg = f"{msg_base}\n\nID: {uuid.uuid4()}"
            final_msg = simulate_typing_effect(unique_msg)

            cl.direct_answer(gc_thread_id, final_msg)
            print(f"✔️ Sent: {final_msg[:40]}...")

            delay = random.randint(25, 40)  # Safe human delay
            time.sleep(delay)

        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(60)

# ▶️ Run spammer
start_gc_autospam()
