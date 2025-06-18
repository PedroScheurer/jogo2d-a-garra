# pip install cx_freeze
import cx_Freeze
includes = [
    "aifc",
    "chunk",
    "audioop",
    "cmath",
    "collections",
    "concurrent",
    "contextlib",
    "ctypes",
    "email",
    "encodings",
    "enum",
    "functools",
    "gzip",
    "hashlib",
    "heapq",
    "html",
    "io",
    "itertools",
    "locale",
    "logging",
    "multiprocessing",
    "operator",
    "os",
    "pathlib",
    "queue",
    "random",
    "re",
    "select",
    "shlex",
    "signal",
    "socket",
    "ssl",
    "struct",
    "subprocess",
    "sys",
    "tempfile",
    "threading",
    "time",
    "traceback",
    "types",
    "unicodedata",
    "warnings",
    "weakref",
    "wave",
    "xml",
    "zipfile"
]
executaveis = [ 
               cx_Freeze.Executable(script="main.py", icon="recursos/icoUrsinho_dourado.ico") ]
cx_Freeze.setup(
    name = "A Garra",
    options={
        "build_exe":{
            "packages":["pygame",
                        "pyttsx3",
                        "speech_recognition",
                        "pyaudio",
                        "random",
                        "math",
                        "threading",
                        "queue"],
            "includes": includes,
            "include_files":["recursos",
                             "log.dat"]
        }
    }, executables = executaveis
)

# python setup.py build
# python setup.py bdist_msi
