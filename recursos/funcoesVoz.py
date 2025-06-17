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
        recognizer.adjust_for_ambient_noise(source)

        while True:
            try:
                print("[OUVIR] Aguardando fala...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                fala = recognizer.recognize_google(audio, language='pt-BR')
                print(f"[OUVIR] Você disse: {fala}")
                falaResultado = fala.lower()
            except controladorVoz.UnknownValueError:
                print("[OUVIR] Não entendi o que foi dito.")
                falaResultado = ""
            except controladorVoz.RequestError:
                print("[OUVIR] Erro ao acessar o serviço de reconhecimento.")
                falaResultado = ""
            except Exception as e:
                print(f"[OUVIR] Erro inesperado: {e}")