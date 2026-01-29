import time

from voice import listen, speak
import commands

from config import ASSISTANT_NAME, WAKE_WORDS, OWNER


time.sleep(1)

speak("Stella is now online and ready.")


sleep_mode = False
running = True


while running:

    try:

        command = listen()

        if not command:
            continue

        print("You:", command)


        # -------- STOP PROGRAM --------
        if "stop" in command:
            speak("Stopping Stella. Goodbye.")
            break


        # -------- SLEEP MODE --------
        if "exit" in command:
            sleep_mode = True
            speak("I am in sleep mode.")
            continue


        # -------- WAKE UP --------
        if sleep_mode:

            if any(w in command for w in WAKE_WORDS):
                sleep_mode = False
                speak("I am awake now.")

            continue


        # Remove name
        if ASSISTANT_NAME in command:
            command = command.replace(ASSISTANT_NAME, "").strip()


        # -------- SHUTDOWN --------
        if "shutdown" in command:
            speak("Shutting down PC.")
            commands.shutdown_pc()
            continue


        # -------- RESTART --------
        if "restart" in command:
            speak("Restarting PC.")
            commands.restart_pc()
            continue


        # -------- SMART COMMANDS --------
        if commands.smart_open(command):
            continue


        # -------- UNKNOWN --------
        speak("Sorry, I did not understand.")


    except Exception as e:

        print("Error:", e)
        speak("Something went wrong.")
