import asyncio
import edge_tts
import speech_recognition as sr
import pygame
import os
import pyttsx3
import threading
import config

is_speaking = False


pygame.mixer.init()

# ---------- OFFLINE ENGINE (BACKUP) ----------
engine = pyttsx3.init("sapi5")

engine.setProperty(
    "voice",
    r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
)

engine.setProperty("rate", 170)

# Lock to prevent multiple threads using pyttsx3 at same time
_speak_lock = threading.Lock()

# Temp file for Edge TTS audio
_EDGE_TTS_FILE = os.path.join(os.path.dirname(__file__), "edge_temp.mp3")


# ---------- EDGE TTS (MAIN) ----------
async def _edge_tts_generate(text):
    """Generate audio using Edge TTS with Michelle voice"""
    communicate = edge_tts.Communicate(text, "en-US-MichelleNeural")
    with open(_EDGE_TTS_FILE, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])


def _edge_speak(text):
    """Play speech using Edge TTS"""
    try:
        asyncio.run(_edge_tts_generate(text))

        if not os.path.exists(_EDGE_TTS_FILE):
            return False

        pygame.mixer.music.load(_EDGE_TTS_FILE)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(30)


        pygame.mixer.music.unload()

        return True

    except Exception as e:
        print("Edge TTS Error:", e)
        return False

    finally:
        if os.path.exists(_EDGE_TTS_FILE):
            try:
                os.remove(_EDGE_TTS_FILE)
            except:
                pass


# ---------- OFFLINE (BACKUP) ----------
def _offline_speak(text):
    engine.say(text)
    engine.runAndWait()


# ---------- THREAD SAFE SPEAK ----------
def speak(text):

    def _run():
        global is_speaking
        is_speaking = True

        with _speak_lock:
            try:
                # Try Edge TTS first (Michelle)
                if _edge_speak(text):
                    pass
                else:
                    print("Falling back to Zira...")
                    _offline_speak(text)

            except Exception as e:
                print("Speak error:", e)
                try:
                    _offline_speak(text)
                except Exception as e2:
                    print("Offline speak error:", e2)

        is_speaking = False

    threading.Thread(target=_run, daemon=True).start()



# ---------- LISTEN ----------
def listen():

    global is_speaking

    if is_speaking:
        return ""

    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    
    
    r.energy_threshold = 300
    r.pause_threshold = 0.8
    r.non_speaking_duration = 0.5

    try:

        with sr.Microphone() as source:

            print("Listening...")

            r.adjust_for_ambient_noise(source, duration=0.2)

            audio = r.listen(
                source,
                timeout=3,
                phrase_time_limit=6
            )

    except:
        return ""

    try:
        text = r.recognize_google(audio, language="en-US").lower()
        return text

    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("Network error - check internet connection")
        return ""
    except:
        return ""


# ---------- HELPER: GET RESPONSE ----------
def get_response(key):
    """Get response by key"""
    return config.RESPONSES.get(key, "")