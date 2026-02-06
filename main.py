import sys
import time
import config
from voice import listen, speak, get_response
import commands

from config import ASSISTANT_NAME, WAKE_WORDS, MIN_PYTHON, MAX_PYTHON


# ---------- Python Version Warning ----------
if not (MIN_PYTHON <= sys.version_info[:2] <= MAX_PYTHON):
    print("⚠️ Best supported Python is 3.10 or 3.11")
    print("⚠️ You are using:", sys.version.split()[0])


# ---------- Startup ----------
time.sleep(0.6)

# time-based greeting
speak(commands.smart_greeting())

# optional startup line
speak(get_response("startup"))


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
        if any(word == command for word in config.COMMANDS_KEYWORDS["stop"]):

            try:
                speak(get_response("stop"))
                time.sleep(4)
            except:
                pass

            print("Stella stopped.")
            break


        # ---------- ONLY NAME ----------
        if command == ASSISTANT_NAME:
            speak(get_response("uhmm"))
            continue


        # ---------- SLEEP MODE ----------
        if any(word in command for word in config.COMMANDS_KEYWORDS["sleep"]):

            sleep_mode = True
            speak(get_response("sleep_mode"))
            continue


        # ---------- WAKE MODE ----------
        if sleep_mode:

            if any(word in command for word in WAKE_WORDS):

                sleep_mode = False
                speak(get_response("wake_up"))

            continue


        # ---------- Remove Assistant Name ----------
        if ASSISTANT_NAME in command:
            command = command.replace(ASSISTANT_NAME, "").strip()


        # ---------- SHUTDOWN ----------
        if any(word in command for word in config.COMMANDS_KEYWORDS["shutdown"]):
            commands.shutdown_pc()
            continue


        # ---------- RESTART ----------
        if any(word in command for word in config.COMMANDS_KEYWORDS["restart"]):
            commands.restart_pc()
            continue
        
        
        # ---------- TIME ----------
        if "time" in command:
            speak(commands.tell_time())
            continue

          # ---------- DATE ----------
        if "date" in command or "today" in command:
            speak(commands.tell_date())
            continue
        
        
                # ---------- BATTERY ----------
        if "battery" in command or "battery status" in command or "charge" in command:
            speak(commands.battery_status())
            continue

        
        
         # ---------- GREETING ----------
        if "good morning" in command or "good afternoon" in command or "good evening" in command or "good night" in command:
            speak(commands.smart_greeting())
            continue

        
        
                # ---------- VOLUME ----------
        if "increase volume" in command or "volume up" in command:
            speak(commands.change_volume("up"))
            continue

        if "decrease volume" in command or "volume down" in command:
            speak(commands.change_volume("down"))
            continue

        if "mute volume" in command or "mute" in command:
            speak(commands.change_volume("mute"))
            continue

        if "unmute volume" in command or "unmute" in command:
            speak(commands.change_volume("unmute"))
            continue

        
        
        
        # ---------- SMART COMMAND ----------
        if commands.smart_open(command):
            continue


        # ---------- UNKNOWN ----------
        speak(get_response("unknown"))


    except Exception as e:

        import traceback
        print("Error:", e)
        print("Full traceback:")
        traceback.print_exc()

        speak(get_response("error"))