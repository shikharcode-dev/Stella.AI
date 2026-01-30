import sys
import time

from voice import listen, speak
import commands

from config import ASSISTANT_NAME, WAKE_WORDS, MIN_PYTHON, MAX_PYTHON


# ---------- Python Version Warning ----------
if not (MIN_PYTHON <= sys.version_info[:2] <= MAX_PYTHON):

    print("⚠️ Best supported Python is 3.10 or 3.11")
    print("⚠️ You are using:", sys.version.split()[0])


# ---------- Startup ----------
time.sleep(1)

speak("Stella is online and ready.")


sleep_mode = False


# ---------- Main Loop ----------
while True:

    try:

        command = listen()

        if not command:
            continue

        command = command.strip().lower()

        print("You:", command)


        # ---------- STOP ----------
        if command == "stop":

            try:
                speak("Stopping Stella. Goodbye.")
                time.sleep(4)   # Wait for voice to finish
            except:
                pass

            print("Stella stopped.")
            break

        # ---------- ONLY NAME ----------
        if command == ASSISTANT_NAME:
            speak("hmm?")
            continue


        # ---------- SLEEP MODE ----------
        if command in ["exit", "sleep"]:

            sleep_mode = True
            speak("Computer is going to sleep mode.")
            continue


        # ---------- WAKE MODE ----------
        if sleep_mode:

            if any(word in command for word in WAKE_WORDS):

                sleep_mode = False
                speak("I am awake and ready.")

            continue


        # ---------- Remove Assistant Name ----------
        if ASSISTANT_NAME in command:

            command = command.replace(ASSISTANT_NAME, "").strip()


        # ---------- SHUTDOWN ----------
        if "shutdown" in command:

            speak("Your computer is shutting down.")
            commands.shutdown_pc()
            continue


        # ---------- RESTART ----------
        if "restart" in command:

            speak("Your computer is restarting.")
            commands.restart_pc()
            continue


        # ---------- SMART COMMAND ----------
        if commands.smart_open(command):
            continue


        # ---------- UNKNOWN ----------
        speak("Sorry, I did not understand that.")


    except Exception as e:

        print("Error:", e)

        speak("Something went wrong. Please try again.")

