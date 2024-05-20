# Установка необходимых библиотек
# pip install -r .\libs.txt

import random
import os
# gtts - для перевода текст в речь.
try:
    from gtts import gTTS
except ImportError:
    print("Для работы этой программы необходимо установить библиотеки:")
    print("gtts")
    print("Вы можете установить их, выполнив следующие команды:")
    print(R"pip install -r .\libs.txt")
    input("> ")
    exit()

error_ai = ["Не удалось получить ответ от нейросети.",
            "Нейросеть не в состоянии ответить.",
            "Ошибка нейросети."
            ]

def text_is_readable(text):
    # Проверка на наличие кириллицы на входе
    import regex
    return regex.search(r'\p{Cyrillic}', text) is not None

def synthesis(text, audio_path):
    print("Начало синтеза текста")
    if text_is_readable(text):
        assistant_say(text, audio_path)
        print("Синтез текста закончен.")
    else:
        # Отрабатывает при непонятном выводе нейросети.
        print("Невозможно разобрать ответ нейросети.")
        assistant_say(random.choice(error_ai), R".\assistant.mp3")
        
def assistant_say(text, audio_path=R".\assistant.mp3"):
    output = gTTS(text=text, lang="ru", slow=False)
    if os.path.exists(audio_path):
        os.remove(audio_path)  # Удаляем существующий файл, если он существует
    output.save(audio_path)
    

if __name__ == "__main__":
    assistant_say("Привет! Я новая помощница.", R".\assistant.mp3")
    with open(R".\input\text", "r", encoding="utf-8") as file:
        text = file.read()
        synthesis(text, "answer.mp3")