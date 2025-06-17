# pip install cx_freeze
import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(script="main.py", icon="recursos/icoUrsinho_dourado.ico") ]
cx_Freeze.setup(
    name = "A Garra",
    options={
        "build_exe":{
            "packages":["pygame",
                        "pyttsx3",
                        "SpeechRecognition",
                        "pyaudio",
                        "random",
                        "math",
                        "threading"],
            "include_files":["recursos",
                             "log.dat"]
        }
    }, executables = executaveis
)

# python setup.py build
# python setup.py bdist_msi
