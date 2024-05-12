# Установка необходимых библиотек
# pip install -r .\libs.txt

# PyAudio - для работы с аудиоустройством.
# wave - для записи аудио в файл WAV.

try:
    import pyaudio
    import wave
except ImportError:
    print("Для работы этой программы необходимо установить библиотеки:")
    print("pyaudio")
    print("wave")
    print("Вы можете установить их, выполнив следующие команды:")
    print(R"pip install -r .\libs.txt")
    input("> ")
    exit()

# Параметры записи звука
CHUNK = 1024 # определяет форму ауди сигнала
FRT = pyaudio.paInt16 # шестнадцатибитный формат задает значение амплитуды
CHAN = 1 # канал записи звука
RT = 44100 # частота 
REC_SEC = 5 #длина записи
OUTPUT = "record.mp3"

p = pyaudio.PyAudio()

stream = p.open(format=FRT, channels=CHAN, 
                rate=RT, input = True,
                frames_per_buffer=CHUNK)
print("Запись.\nГоворите...")

# Начало прослушивания
frames = []
for i in range(0, int(RT / CHUNK * REC_SEC)):
    data = stream.read(CHUNK)
    frames.append(data)
print("Звуковой файл записан.")
# Остановка прослушивания
stream.stop_stream()
stream.close()
p.terminate()

# Запись в файл .wav
w = wave.open(OUTPUT, "wb")
w.setnchannels(CHAN)
w.setsampwidth(p.get_sample_size(FRT))
w.setframerate(RT)
w.writeframes(b''.join(frames))
w.close()