import subprocess
import webbrowser
import pywhatkit
import config
from voice import speak, get_response
from datetime import datetime


# ---------- DESKTOP APPS ----------
DESKTOP_APPS = {
    "vs code": "code",
    "notepad": "notepad",
    "chrome": "chrome",
    "spotify": "spotify",
    "telegram": "telegram",
    "discord": "discord",
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "files": "explorer",
    "file explorer": "explorer"
}


# ---------- STORE / SYSTEM APPS ----------
STORE_APPS = {
    "whatsapp": "whatsapp:",
    "microsoft store": "ms-windows-store:",
    "store": "ms-windows-store:",
    "settings": "ms-settings:",
    "camera": "microsoft.windows.camera:",
    "mail": "outlookmail:",
    "calculator": "calculator:"
}


# ---------- WEBSITES ----------
WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "instagram": "https://www.instagram.com",
    "reddit": "https://www.reddit.com"
}


# ---------- SEARCH ----------
def smart_search(cmd):

    for key in config.COMMANDS_KEYWORDS["search"]:

        if cmd.startswith(key) or key in cmd:

            q = cmd.replace(key, "").strip()

            if not q:
                continue

            speak(f"Searching {q}")

            webbrowser.open(
                f"https://www.google.com/search?q={q.replace(' ', '+')}"
            )

            return True

    return False


# ---------- OPEN APP ----------
def open_any_app(cmd):

    has_open_keyword = False

    for key in config.COMMANDS_KEYWORDS["open"]:
        if key in cmd:
            has_open_keyword = True
            cmd = cmd.replace(key, "").strip()
            break

    if not has_open_keyword:
        return False

    app = cmd.strip()

    if not app:
        return False

    # Desktop apps
    if app in DESKTOP_APPS:

        exe = DESKTOP_APPS[app]

        try:
            speak(f"Opening {app}")

            subprocess.Popen(
                ["cmd", "/c", "start", "", exe],
                shell=True
            )

            return True

        except Exception as e:
            print(f"Desktop app error: {e}")

    # Store / system apps
    if app in STORE_APPS:

        uri = STORE_APPS[app]

        try:
            speak(f"Opening {app}")

            subprocess.Popen(
                ["cmd", "/c", "start", "", uri],
                shell=True
            )

            return True

        except Exception as e:
            print(f"Store app error: {e}")

    # Websites
    if app in WEBSITES:

        url = WEBSITES[app]

        try:
            speak(f"Opening {app}")

            webbrowser.open(url)
            return True

        except Exception as e:
            print(f"Website error: {e}")

    # If app not found
    speak(f"I cannot find {app}")

    return False


# ---------- YOUTUBE ----------
def play_youtube(cmd):

    has_play_keyword = False
    for key in config.COMMANDS_KEYWORDS["play"]:
        if cmd.startswith(key) or key in cmd:
            has_play_keyword = True
            cmd = cmd.replace(key, "").strip()
            break

    if not has_play_keyword:
        return False

    song = cmd.strip()

    if not song:
        return False

    speak(f"Playing {song}")

    pywhatkit.playonyt(song)

    return True


# ---------- SMART ----------
def smart_open(cmd):

    return (
        smart_search(cmd)
        or play_youtube(cmd)
        or open_any_app(cmd)
    )


# ---------- SHUTDOWN ----------
def shutdown_pc():

    speak(get_response("shutdown"))

    subprocess.run(["shutdown", "/s", "/t", "5"])


# ---------- RESTART ----------
def restart_pc():

    speak(get_response("restart"))

    subprocess.run(["shutdown", "/r", "/t", "5"])
    
    
    
    
    
    
# time func. what is time
def tell_time():
    current_time = datetime.now().strftime("%I:%M %p")
    return f"The current time is {current_time}"



# date func. what is today's date
def tell_date():
    today_date = datetime.now().strftime("%A, %d %B %Y")
    return f"Today's date is {today_date}"



# greeting based on time
def smart_greeting():
    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "Good morning!"
    elif 12 <= hour < 17:
        return "Good afternoon!"
    elif 17 <= hour < 22:
        return "Good evening!"
    else:
        return "Good night!"



# battery status
def battery_status():
    try:
        import psutil

        battery = psutil.sensors_battery()

        if battery is None:
            return "Sorry, I cannot detect the battery on this device."

        percent = battery.percent
        charging = battery.power_plugged

        if charging:
            return f"Your battery is at {percent} percent and charging."
        else:
            return f"Your battery is at {percent} percent and not charging."

    except Exception:
        return "Sorry, I am unable to check the battery status right now."




# ---------- VOLUME CONTROL (WINDOWS SAFE METHOD) ----------
def change_volume(action):
    try:
        import pyautogui

        if action == "up":
            for _ in range(5):
                pyautogui.press("volumeup")
            return "Volume increased"

        elif action == "down":
            for _ in range(5):
                pyautogui.press("volumedown")
            return "Volume decreased"

        elif action == "mute":
            pyautogui.press("volumemute")
            return "Volume muted"

        elif action == "unmute":
            pyautogui.press("volumemute")
            return "Volume unmuted"

        return "Volume adjusted"

    except Exception as e:
        print("Volume error:", e)
        return "Sorry, I cannot control the volume."
