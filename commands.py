import subprocess
import platform
import webbrowser
import pywhatkit
import shutil

from voice import speak


APP_PATHS = {
    "vs code": ["code"],
    "notepad": ["notepad"],
    "calculator": ["calc"],
    "chrome": ["chrome"],
    "files": ["explorer", "."]
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

            exe = APP_PATHS[app][0]

            if shutil.which(exe):

                speak(f"Opening {app}")
                subprocess.Popen(exe)

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

    return (
        play_youtube(cmd)
        or open_app(cmd)
        or open_site(cmd)
    )


# ---------- Shutdown ----------
def shutdown_pc():

    speak("Shutting down your computer.")

    system = platform.system()

    if system == "Windows":
        subprocess.run(["shutdown", "/s", "/t", "5"])

    elif system == "Linux":
        subprocess.run(["shutdown", "-h", "now"])

    elif system == "Darwin":
        subprocess.run(["osascript", "-e", 'tell app "System Events" to shut down'])


# ---------- Restart ----------
def restart_pc():

    speak("Restarting your computer.")

    system = platform.system()

    if system == "Windows":
        subprocess.run(["shutdown", "/r", "/t", "5"])

    elif system == "Linux":
        subprocess.run(["reboot"])

    elif system == "Darwin":
        subprocess.run(["osascript", "-e", 'tell app "System Events" to restart'])

