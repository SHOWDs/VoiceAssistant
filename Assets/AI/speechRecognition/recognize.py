import speech_recognition as sr
import random

# Варианты ответов
error_variants = ["Извините, не удалось распознать речь.", 
                  "Вы по-китайски говорите? Пожалуйста, повторите!", 
                  "Не думала, что вы знаете китайский! Я ничего не поняла, пожалуйста повторите!", 
                  "Я ничего не понимаю. Повторите свой запрос!", "Чего-чего? Ничего не понимаю! Пожалуйста, повторите!",
                  "Простите....... повторите!", "Что-то я вас не поняла!",
                  "Извините, но создатель не встроил в меня функцию общения с китайцами! Если без шуток, то повторите Ваш вопрос!"]

silence_variants = ["Я вас не слышу.", "Повторите, пожалуйста.",
                    "Извините, не удалось распознать речь.",
                    "Я вас не расслышала. Повторите."]

access_variants = ["Конечно! Вот что по этому вопросу пишет нейросеть.",
                   "Обрабатываю! Подождите немного.",
                   "Напрягаю все свои извиллины и пытаюсь выдать ответ.",
                   "Работаю. Соединяю вас с нейросетью.",
                   "Мишка фредди прыгает с криками в экран и выдает ответ.",
                   "Минуточку. Спрашиваю нейросеть по этому поводу.",
                   "One moment. Just one moment!",
                   "Uno momento! Uno momento!",
                   "Дайте подумать немного.",
                   "Рассматриваю ваш вопрос.",
                   "Приступаю! Надеюсь, наша нейросеть сегодня в настроении отвечать на вопросы.",
                   "Выполняю ваш запрос.", 
                   "Перенаправляю вопрос нейросети.",
                   "Хорошо. Отправляю запрос нейросети, кажется, она сейчас делает паузу на чашечку кофе."]

def recognize(mp3_path):
    try:
        sample = sr.AudioFile(mp3_path)
    except Exception as e:
        print("Возникла ошибка:", e)
        return random.choice(error_variants), None  # Возвращаем сообщение об ошибке и None

    r = sr.Recognizer()
    with sample as audio:
        try:
            content = r.record(audio)
            r.adjust_for_ambient_noise(audio)
            recognized_text = r.recognize_google(content, language="ru-RU")
            print("Речь удалось распознать.")
            return random.choice(access_variants), recognized_text  # случайное сообщение и распознанный текст
        except sr.UnknownValueError:
            print("Код ошибки: 0")
            return random.choice(silence_variants), "0"  # случайное сообщение о тишине и None
        except sr.RequestError as e:
            print("Код ошибки: -1")
            return "Ошибка", "-1"  # сообщение об ошибке и None

if __name__ == "__main__":
    assistant_answer = recognize(R".\input.mp3")
    print(f"Запрос:\n- {assistant_answer[1].capitalize()}")
    print(f"Незаписанный ответ от ассистента:\n- {str(assistant_answer[0])}")
