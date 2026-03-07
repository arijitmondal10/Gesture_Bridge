import pyttsx3
import threading

engine = pyttsx3.init()

# Adjust voice properties
engine.setProperty('rate', 160)     # Speed of speech (default ~200)
engine.setProperty('volume', 0.9)   # Volume (0.0 to 1.0)

# Optional: choose a better voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):

    def run():
        engine.say(text)
        engine.runAndWait()

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()