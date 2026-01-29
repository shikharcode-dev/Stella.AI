import asyncio
import edge_tts
import speech_recognition as sr
import pygame
import uuid
import os
import pyttsx3


# ================= SETTINGS =================

VOICE = "en-US-JennyNeural"

pygame.mixer.init()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


# ---------- OFFLINE ENGINE (Windows Female) ----------
engine = pyttsx3.init("sapi5")

voices = engine.getProperty("voices")

for v in voices:
    if "female" in v.name.lower() or "zira" in v.name.lower():
        engine.setProperty("voice", v.id)
        break

engine.setProperty("rate", 170)


# ---------- EDGE TEMP ----------
async def _edge_speak(text):

    filename = f"edge_{uuid.uuid4().hex}.mp3"

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

        if os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass


# ---------- GOOGLE BACKUP ----------
def _google_speak(text):

    try:
        from gtts import gTTS

        filename = f"google_{uuid.uuid4().hex}.mp3"

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


# ---------- OFFLINE FEMALE ----------
def _offline_speak(text):

    try:

        engine.say(text)
        engine.runAndWait()
        return True

    except Exception as e:

        print("Offline Error:", e)
        return False


# ---------- MAIN SPEAK ----------
def speak(text):

    try:

        # 1️⃣ TEMP Edge (Best)
        if loop.run_until_complete(_edge_speak(text)):
            return


        # 2️⃣ Offline Female
        if _offline_speak(text):
            return


        # 3️⃣ Google
        if _google_speak(text):
            return


    except:

        _offline_speak(text)


# ---------- LISTEN ----------
def listen():

    r = sr.Recognizer()

    r.energy_threshold = 200
    r.pause_threshold = 0.5

    try:

        with sr.Microphone() as source:

            print("Listening...")

            r.adjust_for_ambient_noise(source, duration=0.2)

            audio = r.listen(source)

    except:
        return ""


    try:
        return r.recognize_google(audio).lower()

    except:
        return ""

