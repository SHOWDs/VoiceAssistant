## Автор кода ##
## Никита Шохов (dabnshowd@gmail.com) ##
import sys
import os
import customtkinter as ctk
import threading

window_width = 500
window_height = 350
STATUS = "Не активен"

dir = os.path.dirname(os.path.abspath(__file__))
ico_path = os.path.join(dir, 'icon', 'icon.ico')
ai_path = sys.path.append(os.path.join(dir, "AI"))

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

# Работа с элементами интерфейса из другого потока
def update_status():
    status_frame.configure(text=f"Статус: {STATUS}")

@run_in_background
def begin():
    global STATUS
    global recording
    
    STATUS = "Активен"
    update_status()  # Обновляем статус в основном потоке Tkinter
    
    try:
        button.configure(fg_color="red")
        button.configure(state="disabled")
        from AI.record import record
        from AI.ai_request import Flow
        recording = True
        record(3, recording)
        flow = Flow()
        flow.flow()
    except ImportError as e:
        print("Не могу найти модуль record.py")
        show_error_message()  # Показываем сообщение об ошибке
    finally:
        print(flow.get().ai_answer)
        STATUS = "Не активен"
        update_status()  # Обновляем статус в основном потоке Tkinter
        button.configure(state="normal")
        button.configure(fg_color="green")
        

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)
root.iconbitmap(ico_path)
root.title("Искусственный Интеллект")

frame = ctk.CTkFrame(master=root)
frame.pack(pady=60, padx=60, fill="both", expand=True)

button = ctk.CTkButton(master=frame, text="Начать запись", command=begin,
                       fg_color="green",
                       width=120,
                       height=32,
                       hover_color="red")
button.pack(pady=(90, 0), padx=10, anchor="center")

status_frame = ctk.CTkLabel(master=frame, text=f"Статус: {STATUS}")
status_frame.pack(pady=0, padx=10, anchor="center")

# Центрируем окно
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2) - 60
root.geometry(f"{width}x{height}+{x}+{y}")

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
