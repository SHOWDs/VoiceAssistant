## Автор кода ##
## Никита Шохов (dabnshowd@gmail.com) ##

# Установка необходимых библиотек
# pip install -r libs.txt

# speech_recognition для распознавания речи
# requests - для отправки данных через Http-форму
# g4f <- Для бесплатной нейросети
# pyaudio <- Для записи файла

import os
import time

try:
    from speechRecognition.recognize import recognize  # Речь в текст
    from speechSynthesis.synthesis import synthesis # Текст в речь
    from speechSynthesis.synthesis import assistant_say
    from ai_request_handler import ai_request
except ImportError as e:
    print(e)
    input("Установите библиотеки с помощью \"pip install -r libs.txt\"\n")
    exit()
except FileNotFoundError as e:
    input(e)
    exit()
except:
    print("?")


API = os.path.join(os.path.dirname(__file__), "config", "API_KEY.txt")
CHAT = os.path.join(os.path.dirname(__file__), "ai_answers.txt")
INPUT = os.path.join(os.path.dirname(__file__), "input.mp3")
ASSISTANT = os.path.join(os.path.dirname(__file__), "assistant.mp3")
AI = os.path.join(os.path.dirname(__file__), "ai_answer.mp3")
print(f"API: {API}")
print(f"CHAT: {CHAT}")
print(f"INPUT: {INPUT}")
print(f"ASSISTANT: {ASSISTANT}")
print(f"AI: {AI}")

def flow():
    try:
        if not(os.path.exists(API)): # Удалить проверку, если используется бесплатная нейросеть
            input("Создайте API_KEY.txt в главном каталоге и добавьте API-ключ, чтобы использовать нейросеть YandexGPT-3.\n(В противном случае используйте бесплатную нейросеть)\n")
            exit(0)
        if not(os.path.exists(INPUT)):
            print("Добавьте input.mp3")
        while not(os.path.exists(INPUT)):
                time.sleep(0.02)
    except KeyboardInterrupt:
        exit(0)
    
    answer = recognize(INPUT) # Возвращает массив [Ответ от нейросети, синтезированный текст]
    user = answer[1]
    assistant = answer[0]

    if answer:
        if user != "0" and user != "-1": # Успешно
            print(f"Распознанный текст: {user}")
            print(f"Ассистент говорит: {assistant}")

            assistant_say(assistant, audio_path=ASSISTANT) # Создает файл assistant.mp3
            ai_answer = ai_request(user, API) # Возвращает ответ нейросети
            print_info(f"Распознанный текст:\n- {user}", f"Ассистент говорит:\n- {assistant}", answer=f"Ответ нейросети:\n- {ai_answer}")
            
            while not(ai_answer):
                time.sleep(0.02)
        
            with open(CHAT, "a", encoding="utf-8") as file: # Открываем файл и записываем диалог
                file.write(f"- {user}\n - {ai_answer}\n")
                file.close()
        
            synthesis(ai_answer, AI)

        elif user == "0":
            assistant_say(assistant)
            print_info(f"Распознанный текст:\n- {user}", f"Ассистент говорит:\n- {assistant}")
        elif user == "-1": # Ошибка синтеза (библиотек)
                ...

def print_info(*args, **kwargs): # 
    for arg in args:
        print(arg)
    if 'answer' in kwargs:
        print(kwargs['answer'])

if __name__ == "__main__":
    flow()
