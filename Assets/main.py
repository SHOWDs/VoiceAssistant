## Автор кода ##
## Никита Шохов (dabnshowd@gmail.com) ##

import sys
import os
import customtkinter as ctk
import threading
import pygame


pygame.mixer.init() # не очищать!

window_width = 600
window_height = 300
CHAT = ""
STATUS = "Не активен"

dir = os.path.dirname(os.path.abspath(__file__))
ico_path = os.path.join(dir, 'icon', 'icon.ico')

ai_path = os.path.join(dir, "AI")
sys.path.append(ai_path)
assistant_path = os.path.join(ai_path, 'assistant.mp3')
ai_answer_path = os.path.join(ai_path, 'ai_answer.mp3')
input_path = os.path.join(ai_path, 'input.mp3')


def show_error_message():
    pass

# Управление ресурсами: освобождаем ресурсы при закрытии окна Tkinter
def on_closing():
    global recording, CHAT, STATUS
    recording = False
    CHAT = ""
    STATUS = ""
    pygame.mixer.music.stop()
    pygame.quit()
    root.destroy()

def run_in_background(func):
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs).start()
    return wrapper

def create_multiline_label(parent, text, max_words_per_line=8):
    labels = []
    words = text.split()
    lines = [" ".join(words[i:i+max_words_per_line]) for i in range(0, len(words), max_words_per_line)]
    for line in lines:
        label = ctk.CTkLabel(master=parent, justify="center", text=line)
        label.pack(padx=5, pady=2, anchor="center")  # Используем pack() для размещения меток
        labels.append(label)
    return labels

# Поменять текст, кнопку
def update_status(**kwargs):
    global CHAT, STATUS
    CHAT = kwargs.get("CHAT", "")
    STATUS = kwargs.get("STATUS", "")
    
    for widget in chat_frame.winfo_children():  # Очищаем все дочерние виджеты в chat_frame
        widget.destroy()

    CHAT_labels = create_multiline_label(chat_frame, CHAT)  # Создаем новые метки для CHAT
    status_label.configure(text=f"Статус: {STATUS}")

# # Обработка переноса текста
# def label_overflow(text):
#     max_words_per_line = 8  # Максимальное количество слов в строке
#     words = text.split()  # Разбиваем текст на слова
#     lines = [" ".join(words[i:i+max_words_per_line]) for i in range(0, len(words), max_words_per_line)]  # Разбиваем слова на строки
#     return "\n".join(lines)  # Возвращаем текст с символами новой строки для переноса на следующую строку

def play_assistant(file):
    pygame.mixer.init()
    try:
        if pygame.mixer.music.get_busy():
            # Если аудио проигрывается, сразу переходим к finally
            pygame.mixer.music.stop()
        
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.remove(file)


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
        button.configure(fg_color="red", state="disabled")
        record(3, recording)
        recording = False
        
        button.configure(fg_color="green")
        update_status(CHAT=CHAT, STATUS=STATUS)
        # if os.path.exists(assistant_path): # Не реализовано - ошибки
        #     threading.Thread(target=play_assistant, args=(assistant_path,)).start()
        flow = Flow().flow()

        if os.path.exists(ai_answer_path):
            threading.Thread(target=play_assistant, args=(ai_answer_path,)).start()

    except ImportError as e:
        print("Не могу найти модуль record.py")
        show_error_message()  # Показываем сообщение об ошибке

    finally:
        STATUS = "Не активен"
        CHAT = flow.ai_answer
        update_status(CHAT=CHAT, STATUS=STATUS)
        button.configure(state="normal", fg_color="green")
        os.remove(input_path)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)
root.iconbitmap(ico_path)
root.title("Ассистент")

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

# Центрируем окно
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2) - 60
root.geometry(f"{width}x{height}+{x}+{y}")

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
