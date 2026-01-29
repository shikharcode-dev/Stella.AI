import time

from voice import listen, speak
import commands
from config import ASSISTANT_NAME


time.sleep(1)

speak("Hello, I am Stella. I am ready.")


sleep_mode = False


while True:

    command = listen()

    if not command:
        continue

    print("You:", command)


    # Remove name
    if ASSISTANT_NAME in command:
        command = command.replace(ASSISTANT_NAME, "").strip()


    # ---------- Sleep Mode ----------
    if sleep_mode:

        if "wake up" in command or "hey stella" in command:
            sleep_mode = False
            speak("Yes, I am ready now")

        continue


    # ---------- Stop / Pause ----------
    if "stop" in command or "exit" in command:
        sleep_mode = True
        speak("I am going to sleep")
        continue


    # ---------- Shutdown ----------
    if "shutdown" in command or "shut down" in command:
        commands.shutdown_pc()
        continue


    # ---------- Restart ----------
    if "restart" in command:
        commands.restart_pc()
        continue


    # ---------- Smart System ----------
    if commands.smart_open(command):
        continue


    # ---------- Unknown ----------
    speak("Sorry, I did not understand")

