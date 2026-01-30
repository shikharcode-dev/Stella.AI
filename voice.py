import asyncio
import edge_tts
import speech_recognition as sr
import pygame
import uuid
import os
import pyttsx3
import threading


VOICE = "en-US-JennyNeural"

pygame.mixer.init()


# ---------- OFFLINE ENGINE (MAIN) ----------
engine = pyttsx3.init("sapi5")

voices = engine.getProperty("voices")

for v in voices:
    if "zira" in v.name.lower() or "female" in v.name.lower():
        engine.setProperty("voice", v.id)
        break

engine.setProperty("rate", 170)


# ---------- EDGE (OPTIONAL) ----------
async def _edge_speak(text):

    filename = "edge_temp.mp3"   # One fixed file

    try:

        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(filename)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)

        pygame.mixer.music.unload()

        return True


    except Exception as e:

        print("Edge Error:", e)
        return False


    finally:

        # Always delete
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass

# ---------- GOOGLE ----------
def _google_speak(text):

    try:
        from gtts import gTTS

        filename = "google_temp.mp3"   # One fixed file

        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(filename)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pass

        pygame.mixer.music.unload()

        os.remove(filename)

        return True


    except Exception as e:

        print("Google Error:", e)
        return False


# ---------- OFFLINE ----------
def _offline_speak(text):

    engine.say(text)
    engine.runAndWait()


# ---------- THREAD SAFE SPEAK ----------
def speak(text):

    def _run():

        try:

            # Try Edge once only
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                if loop.run_until_complete(_edge_speak(text)):
                    return
            except:
                pass


            # Try Google
            if _google_speak(text):
                return


            # Always fallback
            _offline_speak(text)

        except:

            _offline_speak(text)


    threading.Thread(target=_run, daemon=True).start()


# ---------- LISTEN ----------
def listen():

    r = sr.Recognizer()

    # Balanced speed + accuracy
    r.energy_threshold = 150
    r.pause_threshold = 0.5
    r.non_speaking_duration = 0.4


    try:

        with sr.Microphone() as source:

            print("Listening...")

            # Quick calibration
            r.adjust_for_ambient_noise(source, duration=0.2)

            audio = r.listen(
                source,
                timeout=4,            # Wait for speech
                phrase_time_limit=10  # Allow long sentences
            )

    except:
        return ""


    try:
        return r.recognize_google(audio).lower()

    except:
        return ""
    
    