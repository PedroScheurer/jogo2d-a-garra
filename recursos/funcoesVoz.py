import pyttsx3, threading
import speech_recognition as controladorVoz

def falar(texto, nome):
    def executarFala():
        engine = pyttsx3.init()
        engine.say(f"{texto}{nome}")
        engine.runAndWait()
    threading.Thread(target=executarFala, daemon=True).start()

def ouvir():
    global falaResultado
    recognizer = controladorVoz.Recognizer()
    with controladorVoz.Microphone() as source:
        print("Diga Algo...")
        print("Fique em silêncio para finalizar!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            falaResultado = recognizer.recognize_google(audio, language='pt-BR')
            print(f"Você disse: {falaResultado}")
        except controladorVoz.UnknownValueError:
            falaResultado = ""
        except controladorVoz.RequestError:
            falaResultado = ""