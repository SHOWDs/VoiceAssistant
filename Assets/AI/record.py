# Установка необходимых библиотек
# pip install -r .\libs.txt

# PyAudio - для работы с аудиоустройством.
# wave - для записи аудио в файл WAV.

import os
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
CHUNK = 1024 # определяет форму аудио сигнала
FRT = pyaudio.paInt16 # шестнадцатибитный формат задает значение амплитуды
CHAN = 1 # канал записи звука
RT = 44100 # частота 
REC_TIME = 0 #длина записи
OUTPUT = dir = os.path.join(os.path.dirname(__file__), "input.mp3")

def record(REC_TIME:int, recording:bool=True):
    p = pyaudio.PyAudio()

    stream = p.open(format=FRT, channels=CHAN, 
                    rate=RT, input = True,
                    frames_per_buffer=CHUNK)
    print("Говорите...")

    # Начало прослушивания
    frames = []
    for i in range(0, int(RT / CHUNK * REC_TIME)):
        try:
            if recording:
                data = stream.read(CHUNK)
                frames.append(data)
            else:
                break
        except KeyboardInterrupt:
            exit(0)
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

if __name__ == "__main__":
    record()