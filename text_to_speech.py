import pyttsx3
import threading

def speak(text):

    def run():
        engine = pyttsx3.init()

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # female voice
        engine.setProperty('rate', 140)
        engine.setProperty('volume', 0.9)

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()