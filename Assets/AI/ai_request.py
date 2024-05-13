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

class Flow():
    def __init__(self):
        self.answer = ""
        self.user = ""
        self.assistant = ""
        self.ai_answer = ""
    
    def flow(self):
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
        
        self.answer = recognize(INPUT) # Возвращает массив [Ответ от нейросети, синтезированный текст]
        self.assistant = self.answer[0]
        self.user = self.answer[1]

        if self.answer:
            if self.user != "0" and self.user != "-1": # Успешно
                print(f"Распознанный текст: {self.user}")
                print(f"Ассистент говорит: {self.assistant}")

                assistant_say(self.assistant, audio_path=ASSISTANT) # Создает файл assistant.mp3
                self.ai_answer = ai_request(self.user, API) # Возвращает ответ нейросети
                # self.print_info(f"Распознанный текст:\n- {self.user}", f"Ассистент говорит:\n- {self.assistant}", answer=f"Ответ нейросети:\n- {self.ai_answer}")
                
                while not(self.ai_answer):
                    time.sleep(0.02)
            
                with open(CHAT, "a", encoding="utf-8") as file: # Открываем файл и записываем диалог
                    file.write(f"- {self.user}\n - {self.ai_answer}\n")
                    file.close()
            
                synthesis(self.ai_answer, AI)
                self.print_info("Цикл закончен")

            elif self.user == "0":
                assistant_say(self.assistant)
                # self.print_info(f"Распознанный текст:\n- {self.user}", f"Ассистент говорит:\n- {self.assistant}")
            elif self.user == "-1": # Ошибка синтеза (библиотек)
                    ...
        return self

    def print_info(self, *args, **kwargs):
        for arg in args:
            print(arg)
        if 'answer' in kwargs:
            print(kwargs['answer'])
        
    def get(self):
        return self
# get_info().answer
# get_info().user
# get_info().assistant
if __name__ == "__main__":
    main = Flow()
    main.flow()
    
    print(main.get().ai_answer)
