import asyncio
import edge_tts
import speech_recognition as sr
import pygame
import uuid
import os


VOICE = "en-US-JennyNeural"


pygame.mixer.init()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def _speak(text):

    filename = f"voice_{uuid.uuid4().hex}.mp3"

    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(filename)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

    pygame.mixer.music.unload()
    os.remove(filename)


def speak(text):
    loop.run_until_complete(_speak(text))


def listen():
    r = sr.Recognizer()

    r.energy_threshold = 200
    r.pause_threshold = 0.5
    r.dynamic_energy_threshold = True

    with sr.Microphone() as source:

        print("Listening...")

        r.adjust_for_ambient_noise(source, duration=0.15)

        try:
            audio = r.listen(source, timeout=None)
        except sr.WaitTimeoutError:
            return ""

    try:
        return r.recognize_google(audio).lower()
    except:
        return ""
