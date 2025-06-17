import pyttsx3, threading
import speech_recognition as controladorVoz
from queue import Queue
fila_falas = Queue()


def falar(texto, nome):
    def executarFala():
        engine = pyttsx3.init()
        engine.say(f"{texto}{nome}")
        engine.runAndWait()
    threading.Thread(target=executarFala, daemon=True).start()

def ouvir():
    recognizer = controladorVoz.Recognizer()
    with controladorVoz.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)

        while True:
            try:
                print("[OUVIR] Aguardando fala...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                fala = recognizer.recognize_google(audio, language='pt-BR')
                print(f"[OUVIR] Você disse: {fala}")
                fila_falas.put(fala.lower().strip())
            except controladorVoz.UnknownValueError:
                print("[OUVIR] Não entendi o que foi dito.")
            except controladorVoz.RequestError:
                print("[OUVIR] Erro ao acessar o serviço de reconhecimento.")
            except Exception as e:
                print(f"[OUVIR] Erro inesperado: {e}")