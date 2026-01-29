import os
import webbrowser
import re
import pywhatkit

from voice import speak


# ---------- Apps ----------
APP_PATHS = {
    "vs code": "code",
    "vscode": "code",
    "visual studio code": "code",
    "calculator": "calc",
    "notepad": "notepad",
    "files": "explorer",
    "file explorer": "explorer",
    "chrome": "chrome"
}


# ---------- Known Sites ----------
KNOWN_SITES = {
    "google": "google.com",
    "gmail": "mail.google.com",
    "facebook": "facebook.com",
    "instagram": "instagram.com",
    "twitter": "twitter.com",
    "linkedin": "linkedin.com",
    "amazon": "amazon.in",
    "chatgpt": "chat.openai.com",
    "youtube": "youtube.com"
}


# ---------- Clean Text ----------
def clean_text(text):
    text = text.lower()
    text = text.replace(" ", "")
    return text


# ---------- Open App ----------
def open_app(command):

    for app in APP_PATHS:
        if app in command:
            speak(f"Opening {app}")
            os.system(APP_PATHS[app])
            return True

    return False


# ---------- Open Website ----------
def open_website(command):

    clean = clean_text(command)

    # Known sites
    for site in KNOWN_SITES:

        if site in command or clean_text(site) in clean:

            url = "https://" + KNOWN_SITES[site]

            speak(f"Opening {site}")
            webbrowser.open(url)
            return True


    # Any .com .in .gov
    match = re.search(r"([a-zA-Z0-9\-]+)\.(com|in|gov)", command)

    if match:

        site = match.group(0)

        url = "https://" + site

        speak(f"Opening {site}")
        webbrowser.open(url)
        return True


    return False


# ---------- Play YouTube ----------
def play_youtube(command):

    if "play" in command:

        video = command
        video = video.replace("play", "")
        video = video.replace("on youtube", "")
        video = video.replace("youtube", "")
        video = video.strip()

        if video:
            speak(f"Playing {video} on YouTube")
            pywhatkit.playonyt(video)
            return True

    return False


# ---------- Smart System ----------
def smart_open(command):

    if play_youtube(command):
        return True

    if open_app(command):
        return True

    if open_website(command):
        return True

    return False


# ---------- Shutdown ----------
def shutdown_pc():
    speak("Shutting down your computer")
    os.system("shutdown /s /t 5")


# ---------- Restart ----------
def restart_pc():
    speak("Restarting your computer")
    os.system("shutdown /r /t 5")
