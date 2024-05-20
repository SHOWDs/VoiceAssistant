## Автор кода ##
## Никита Шохов (dabnshowd@gmail.com) ##

# Установка необходимых библиотек
# pip install -r libs.txt

import os
import time
import threading

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
URI = os.path.join(os.path.dirname(__file__), "config", "URI.txt")
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
        self.answer_length = 1
    
    def flow(self, answer_length):
        try:
            if not(os.path.exists(API)) or not(os.path.exists(URI)): # Удалить проверку, если используется бесплатная нейросеть
                input("Создайте API_KEY.txt, URI.txt в главном каталоге и добавьте API-ключ, URI, чтобы использовать нейросеть YandexGPT-3.\n(В противном случае используйте бесплатную нейросеть)\n")
                exit(0)
            else:
                try:
                    with open(API, "r", encoding="utf-8") as api_file:
                        api_key = api_file.read()
                        if len(api_key) == 0:
                            input("Вставьте API-ключ в файл API_KEY.txt, чтобы использовать бесплатную нейросеть YandexGPT-3\n")
                            exit("Невозможно получить API-ключ")
                    with open(URI, "r", encoding="utf-8") as uri_file:
                        uri_key = uri_file.read()
                        if len(uri_key) == 0:
                            input("Вставьте URI в файл URI.txt, чтобы использовать бесплатную нейросеть YandexGPT-3\n")
                            exit("Невозможно получить URI.")
                except FileNotFoundError :
                    input("Файл не найден. (Добавьте файл с API-ключом и файл с URI, чтобы использовать бесплатную нейросеть YandexGPT-3)")
                    exit("Невозможно получить API-ключ или URI.")
            if not(os.path.exists(INPUT)):
                print("Добавьте input.mp3")
            while not(os.path.exists(INPUT)):
                    time.sleep(0.02)
        except KeyboardInterrupt:
            exit(0)
        
        self.answer = recognize(INPUT) # Возвращает массив [Ответ от нейросети, синтезированный текст]
        self.assistant = self.answer[0]
        self.user = self.answer[1]
        self.answer_length = answer_length

        if self.answer:
            if self.user != "0" and self.user != "-1": # Успешно
                print(f"Распознанный текст: {self.user}")
                print(f"Ассистент говорит: {self.assistant}")

                threading.Thread(target=self.assistant_say_async, args=(self.assistant, ASSISTANT)).start()
                self.ai_answer = ai_request(self.user, API, URI, self.answer_length) # Возвращает ответ нейросети
                # self.print_info(f"Распознанный текст:\n- {self.user}", f"Ассистент говорит:\n- {self.assistant}", answer=f"Ответ нейросети:\n- {self.ai_answer}")
                
                while not(self.ai_answer):
                    time.sleep(0.02)
            
                with open(CHAT, "a", encoding="utf-8") as file: # Открываем файл и записываем диалог
                    file.write(f"- {self.user}\n - {self.ai_answer}\n")
                    file.close()
            
                synthesis(self.ai_answer, AI)

            elif self.user == "0":
                assistant_say(self.assistant, ASSISTANT)
                # self.print_info(f"Распознанный текст:\n- {self.user}", f"Ассистент говорит:\n- {self.assistant}")
            elif self.user == "-1": # Ошибка синтеза (библиотек)
                    ...
        return self

    def assistant_say_async(self, text, path):
        # Ваш существующий код метода assistant_say здесь
        assistant_say(text, path)  # Здесь text - это аргумент метода, переданный как позиционный


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
    
    print(main.flow().ai_answer)
