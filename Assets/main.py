## Автор кода ##
## Никита Шохов (dabnshowd@gmail.com) ##
import sys
import os
import customtkinter as ctk
import threading


dir = os.path.dirname(os.path.abspath(__file__))
ico_path = os.path.join(dir, 'icon', 'icon.ico')
ai_path = sys.path.append(os.path.join(dir, "AI"))

window_x = 500
window_y = 350

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.geometry(f"{window_x}x{window_y}")
root.resizable(False, False)
root.iconbitmap(ico_path)
root.title("Искусственный Интеллект")

global STATUS
STATUS = "Не активен"

def run_in_background(func):
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs).start()
    return wrapper

@run_in_background
def begin():
    # Отключаем кнопку
    button.configure(state="disabled")
    global STATUS
    STATUS = "Активен"
    try:
        from AI.record import record
        from AI.ai_request import flow
        record()
        flow()
    except ImportError as e:
        print("Не могу найти модуль record.py")
    finally:
        # Включаем кнопку обратно
        button.configure(state="normal")

frame = ctk.CTkFrame(master=root)
frame.pack(pady=60, padx=60, fill="both", expand=True)

button = ctk.CTkButton(master=frame, text="Начать Цикл", command=begin)
button.pack(pady=(100, 0), padx=10, anchor="center")

status_frame = ctk.CTkLabel(master=frame, text=f"Статус: {STATUS}")
status_frame.pack(pady=0, padx=10, anchor="center")

# Центрируем окно
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2) - 60
root.geometry(f"{width}x{height}+{x}+{y}")

root.mainloop()
