import subprocess
import platform
import webbrowser
import pywhatkit
import os

from voice import speak


APP_PATHS = {
    "vs code": "code",
    "notepad": "notepad",
    "calculator": "calc",
    "chrome": "chrome",
    "files": "explorer"
}


SITES = {
    "google": "https://google.com",
    "youtube": "https://youtube.com",
    "gmail": "https://mail.google.com",
    "instagram": "https://instagram.com"
}


# ---------- Apps ----------
def open_app(cmd):

    for app in APP_PATHS:

        if app in cmd:
            speak(f"Opening {app}")
            os.system(APP_PATHS[app])
            return True

    return False


# ---------- Websites ----------
def open_site(cmd):

    for site in SITES:

        if site in cmd:
            speak(f"Opening {site}")
            webbrowser.open(SITES[site])
            return True

    return False


# ---------- YouTube ----------
def play_youtube(cmd):

    if "play" in cmd:

        song = cmd.replace("play", "").strip()

        if song:
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)
            return True

    return False


# ---------- Smart ----------
def smart_open(cmd):

    if play_youtube(cmd):
        return True

    if open_app(cmd):
        return True

    if open_site(cmd):
        return True

    return False


# ---------- Shutdown ----------
def shutdown_pc():

    speak("Shutting down your computer.")

    system = platform.system()

    if system == "Windows":
        subprocess.run(["shutdown", "/s", "/t", "5"])

    else:
        subprocess.run(["shutdown", "-h", "now"])


# ---------- Restart ----------
def restart_pc():

    speak("Restarting your computer.")

    system = platform.system()

    if system == "Windows":
        subprocess.run(["shutdown", "/r", "/t", "5"])

    else:
        subprocess.run(["reboot"])
