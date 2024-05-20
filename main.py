## Автор кода ##
## Никита Шохов (dabnshowd@gmail.com) ##

# Установка необходимых библиотек
# pip install -r libs.txt

import sys
import os
import customtkinter as ctk
import threading
import pygame


pygame.mixer.init() # не очищать!
# Инициализация путей
dir = os.path.dirname(os.path.abspath(__file__))
ico_path = os.path.join(dir, 'icon', 'icon.ico')
ai_path = os.path.join(dir, "AI")
sys.path.append(ai_path)
assistant_path = os.path.join(ai_path, 'assistant.mp3')
ai_answer_path = os.path.join(ai_path, 'ai_answer.mp3')
input_path = os.path.join(ai_path, 'input.mp3')

# Параметры окна
window_width = 600
window_height = 400
answer_length = 1
# Состояние окна
CHAT = ""
STATUS = "Не активен"

# При закрытии окна
def on_closing():
    global recording, CHAT, STATUS
    recording = False
    CHAT = ""
    STATUS = ""
    pygame.mixer.init() # Постоянная инициализация необходима, чтобы pygame не выдавал ошибок при внезапных остановках
    pygame.mixer.music.stop()
    pygame.quit()
    root.destroy()

# Функция запуска параллельных потоков
def run_in_background(func):
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs).start()
    return wrapper

# Функция деления длинной строки на строки
def create_multiline_label(parent, text, max_words_per_line=8):
    labels = []
    words = text.split()
    lines = [" ".join(words[i:i+max_words_per_line]) for i in range(0, len(words), max_words_per_line)]
    for line in lines:
        label = ctk.CTkLabel(master=parent, justify="center", text=line)
        label.pack(padx=5, pady=2, anchor="center")
        labels.append(label)
    return labels

# Функция изменения текста в окне 
def update_status(**kwargs):
    global CHAT, STATUS
    CHAT = kwargs.get("CHAT", "")
    STATUS = kwargs.get("STATUS", "")
    
    for widget in chat_frame.winfo_children():  # Очищаем все дочерние виджеты в chat_frame
        widget.destroy()

    # правильное отображение текста в окне программы (экспериментально)
    create_multiline_label(chat_frame, CHAT)  # Создаем новые метки для CHAT
    status_label.configure(text=f"Статус: {STATUS}")

# Функция воспроизведения mp3 файла.
def play_assistant(file):
    try:
        pygame.mixer.init() # Постоянная инициализация необходима, чтобы pygame не выдавал ошибок при внезапных остановках
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        pygame.mixer.init()
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.remove(file)

# При нажатии на кнопку.
@run_in_background
def begin():
    from AI.record import record
    from AI.ai_request import Flow
    
    global CHAT
    global STATUS
    global recording
    
    recording = True
    
    CHAT = "...:"
    STATUS = "Обработка"
    
    update_status(STATUS=STATUS, CHAT=CHAT)  # Обновляем статус в основном потоке Tkinter
    
    try:
        pygame.mixer.init() # Постоянная инициализация необходима, чтобы pygame не выдавал ошибок при внезапных остановках
        pygame.mixer.music.stop()
        button.configure(fg_color="red", state="disabled")
        record(3, recording)
        recording = False
        
        button.configure(fg_color="green")
        update_status(CHAT=CHAT, STATUS=STATUS)
        # if os.path.exists(assistant_path): # Не реализовано - ошибки
        #     threading.Thread(target=play_assistant, args=(assistant_path,)).start()
        flow = Flow().flow(answer_length)

        if os.path.exists(ai_answer_path):
            threading.Thread(target=play_assistant, args=(ai_answer_path,)).start()

    except ImportError as e:
        input("Не могу найти модуль record.py")
        on_closing()

    finally:
        STATUS = "Не активен"
        CHAT = flow.ai_answer
        update_status(CHAT=CHAT, STATUS=STATUS)
        button.configure(state="normal", fg_color="green")
        os.remove(input_path)


# Инициализация окна
root = ctk.CTk()
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)
root.iconbitmap(ico_path)
root.title("Ассистент (бета)")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Рамка истории ответов
chat_frame = ctk.CTkFrame(master=root)
chat_frame.pack(pady=(20, 0), padx=20, fill="x")
chat_label = ctk.CTkLabel(master=chat_frame, justify="left", text=f"Нажмите на кнопку и отправьте запрос нейросети!")
chat_label.pack(pady=30, padx=10, fill="both", anchor=ctk.CENTER)

# Кнопка для отправки запроса
button_frame = ctk.CTkFrame(master=root)
button_frame.pack(pady=(20, 0), padx=20, fill="x")
button = ctk.CTkButton(master=button_frame, text="Начать запись", command=begin,
                       fg_color="green",
                       width=120,
                       height=30,
                       hover_color="red")
button.pack(pady=(15, 0), padx=0, fill="y")

# Лейбл статуса
status_label = ctk.CTkLabel(master=button_frame, text=f"Статус: {STATUS}")
status_label.pack(pady=(0, 5), padx=0, fill="both")

width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2) - 60
root.geometry(f"{width}x{height}+{x}+{y}")
root.update_idletasks()

# Создание рамки для текста и выпадающего меню
length_frame = ctk.CTkFrame(master=root)
length_frame.pack(pady=(20, 5), padx=20, fill="both")

# Лейбл выпадающего меню
length_label = ctk.CTkLabel(master=length_frame, text="Длина ответа нейросети:")
length_label.pack(pady=0, padx=20, fill="x")

# Создание списка вариантов для длины ответа
response_lengths = ["1", "2", "3", "4", "5"]

# Переменная для хранения выбранной длины ответа
selected_length = ctk.StringVar()
selected_length.set(response_lengths[0])  # Устанавливаем значение по умолчанию

# Функция для обработки изменения выбора в меню
def on_length_change(*args):
    global answer_length
    answer_length = selected_length.get()
    print("Выбранная длина ответа:", answer_length)

selected_length.trace_add("write", on_length_change)  # Добавляем обработчик изменения значения

# Компонент выпадающего меню
length_menu = ctk.CTkOptionMenu(master=length_frame, variable=selected_length, values=response_lengths, fg_color="green")
length_menu.pack(pady=(20, 10), padx=20, fill="y")

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
