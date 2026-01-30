import subprocess
import platform
import webbrowser
import pywhatkit

from voice import speak


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
    "files": "explorer"
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


# ---------- SEARCH ----------
def smart_search(cmd):

    for key in ["search", "find", "look up"]:

        if cmd.startswith(key):

            q = cmd.replace(key, "").strip()

            speak(f"Searching {q}")

            webbrowser.open(
                f"https://www.google.com/search?q={q.replace(' ', '+')}"
            )

            return True

    return False


# ---------- OPEN APP ----------
def open_any_app(cmd):

    if not cmd.startswith("open "):
        return False

    app = cmd.replace("open", "").strip()


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

        except:
            pass


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

        except:
            pass


    speak(f"I cannot find {app}")
    return False


# ---------- YOUTUBE ----------
def play_youtube(cmd):

    if cmd.startswith("play "):

        song = cmd.replace("play", "").strip()

        speak(f"Playing {song}")

        pywhatkit.playonyt(song)

        return True

    return False


# ---------- SMART ----------
def smart_open(cmd):

    return (
        smart_search(cmd)
        or play_youtube(cmd)
        or open_any_app(cmd)
    )


# ---------- SHUTDOWN ----------
def shutdown_pc():

    speak("Shutting down your computer.")

    subprocess.run(["shutdown", "/s", "/t", "5"])


# ---------- RESTART ----------
def restart_pc():

    speak("Restarting your computer.")

    subprocess.run(["shutdown", "/r", "/t", "5"])


