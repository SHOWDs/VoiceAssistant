## Автор кода ##
## Никита Шохов (dabnshowd@gmail.com) ##
import sys
import os
import customtkinter as ctk
import threading

window_width = 600
window_height = 500
CHAT = ""
STATUS = "Не активен"

dir = os.path.dirname(os.path.abspath(__file__))
ico_path = os.path.join(dir, 'icon', 'icon.ico')

ai_path = os.path.join(dir, "AI")
sys.path.append(ai_path)
assistant_path = os.path.join(ai_path, 'assistant.mp3')
ai_answer_path = os.path.join(ai_path, 'ai_answer.mp3')


def show_error_message():
    # Реализуйте ваше сообщение об ошибке здесь
    pass

def run_in_background(func):
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs).start()
    return wrapper

# Управление ресурсами: освобождаем ресурсы при закрытии окна Tkinter
def on_closing():
    global recording
    recording = False
    root.destroy()


def create_multiline_label(parent, text, max_words_per_line=8):
    chat_label.place(x=0, y=0)
    words = text.split()  # Разбиваем текст на слова
    lines = [" ".join(words[i:i+max_words_per_line]) for i in range(0, len(words), max_words_per_line)]  # Разбиваем слова на строки
    labels = []
    for line in lines:
        label = ctk.CTkLabel(master=parent, justify="center", text=line)
        label.pack(padx=5, anchor="center")
        labels.append(label)
    return labels

# Обновленный update_status()
def update_status(**kwargs):
    global CHAT, STATUS
    CHAT = kwargs.get("CHAT", "")
    STATUS = kwargs.get("STATUS", "")
    CHAT_labels = create_multiline_label(chat_frame, CHAT)  # Создаем многострочную метку для CHAT
    chat_label.configure(text="")  # Очищаем основную метку, так как она будет заменена
    chat_label.pack_forget()  # Удаляем основную метку из текущего расположения
    for label in CHAT_labels:
        label.pack(pady=3)  # Добавляем новые многострочные метки
    status_label.configure(text=f"Статус: {STATUS}")

# Обработка переноса текста
def label_overflow(text):
    max_words_per_line = 8  # Максимальное количество слов в строке
    words = text.split()  # Разбиваем текст на слова
    lines = [" ".join(words[i:i+max_words_per_line]) for i in range(0, len(words), max_words_per_line)]  # Разбиваем слова на строки
    return "\n".join(lines)  # Возвращаем текст с символами новой строки для переноса на следующую строку

def play_assistant(file):
    import pygame
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

@run_in_background
def begin():
    global CHAT
    global STATUS
    global recording
    
    STATUS = "Идет запись.."
    update_status(STATUS=STATUS, CHAT=CHAT)  # Обновляем статус в основном потоке Tkinter
    
    try:
        button.configure(fg_color="red")
        button.configure(state="disabled")
        from AI.record import record
        from AI.ai_request import Flow
        recording = True
        record(3, recording)
        STATUS = "Обработка"
        button.configure(fg_color="green")
        update_status(CHAT=CHAT, STATUS=STATUS)
        flow = Flow().flow()
        if os.path.exists(assistant_path):
            play_assistant(assistant_path)
        if os.path.exists(ai_answer_path):
            play_assistant(ai_answer_path)
    except ImportError as e:
        print("Не могу найти модуль record.py")
        show_error_message()  # Показываем сообщение об ошибке
    finally:
        STATUS = "Не активен"
        CHAT = flow.ai_answer
        update_status(CHAT=CHAT, STATUS=STATUS)
        button.configure(state="normal")
        button.configure(fg_color="green")
        

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)
root.iconbitmap(ico_path)
root.title("Ассистент")

# История ответов нейросети
chat_frame = ctk.CTkFrame(master=root)
chat_frame.pack(pady=(20, 90), padx=80, fill="x", expand=True)
chat_label = ctk.CTkLabel(master=chat_frame, justify="left", text=f"...: {CHAT}")
chat_label.pack(pady=30, padx=10, fill="both", anchor=ctk.CENTER)

# Кнопка для отправки запроса
button_frame = ctk.CTkFrame(master=root)
button_frame.pack(pady=(120, 0), padx=0, fill="both", expand=True)
button = ctk.CTkButton(master=button_frame, text="Начать запись", command=begin,
                       fg_color="green",
                       width=120,
                       height=30,
                       hover_color="red")
button.pack(pady=(120, 0), padx=0, anchor="n")

status_label = ctk.CTkLabel(master=button_frame, text=f"Статус: {STATUS}")
status_label.pack(pady=0, padx=0, anchor="center")

# Центрируем окно
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2) - 60
root.geometry(f"{width}x{height}+{x}+{y}")

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
