# !! Чтобы использовать бесплатную нейросеть, требуется добавить библиотеку g4f !!
# Предоставляю код бесплатной нейросети

# import asyncio # pip install nest_asyncio
# from g4f.client import Client
# client = Client()
# answer = ""
    
# def ai_request(text):
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     prompt = "Расскажи в 1 предложении: " + text
#     print(prompt)

#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": prompt}]
#     )
    
#     answer = response.choices[0].message.content
    
#     if "流量" in answer or len(answer) < 2:
#         ai_request(text)
#     else:
#         print(answer)
#         with open(R".\ai_answers.txt", "a", encoding="utf-8") as file:
#             file.writelines(f"{text}: {answer}\n")
#         file.close()
#         return answer

# if __name__ == "__main__":
#     print(ai_request("Как вкусно пожарить мясо без корочки?"))


import requests
import json

def ai_request(text, ai_path):
    try:
        with open(ai_path, "r", encoding="utf-8") as file:
            api_key = file.read()
            if len(api_key) == 0:
                input("Вставьте API-ключ в файл API_KEY.txt, чтобы использовать бесплатную нейросеть YandexGPT-3\n")
                exit("Невозможно получить API-ключ")
    except FileNotFoundError :
        input("Файл не найден. (Добавьте файл с API-ключом, чтобы использовать бесплатную нейросеть YandexGPT-3)")
        exit("Невозможно получить API-ключ")
    
    system_text = "Ты гениальная нейросеть, рассказывающая каждый запрос пользователя в одном-двух предложениях."
    user_text = "Ответь в 1 предложении: " + text
    temperature = 0.0 # от 0.0 до 1.0
    
    prompt = {
        "modelUri": "gpt://b1gqjh6bupu39k4h8i25/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": temperature,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": system_text
            },
            {
                "role": "user",
                "text": user_text
            },
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key " + api_key
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.text
    data_dict = json.loads(result)["result"]["alternatives"][0]["message"]["text"] # Достаем из result содержимое ответа
    answer = formatting(data_dict)
    
    return answer

def formatting(text:str, delete_commas=True, delete_stars=True):
    if delete_stars and "*" in text:
        text = text.replace("*", "")
    if delete_commas and "," in text:
        for i in range(4): # Чтобы чуть укоротить ответ (запятые замедляют ответ примерно на 0.4 секунды)
            text = text.replace(",", "")
    return text


if __name__ == "__main__":
    questions = [
    "Какие технологии лучше всего подходят для разработки мобильных приложений?",
    "Какие книги по искусственному интеллекту вы можете порекомендовать?",
    "Каковы основные принципы работы нейронных сетей?",
    "Какой язык программирования лучше использовать для анализа данных?",
    "Какие существуют методы оптимизации глубоких нейронных сетей?",
    "Какие алгоритмы используются для обработки изображений?",
    "Что такое рекуррентные нейронные сети и в каких областях они применяются?",
    "Какие существуют методы для борьбы с переобучением в машинном обучении?",
    "Какие библиотеки Python наиболее популярны для работы с нейронными сетями?",
    "Какие существуют подходы к аугментации данных в обучении нейронных сетей?",
    "Какие алгоритмы используются для кластеризации данных?",
    "Какие методы машинного обучения можно использовать для прогнозирования временных рядов?",
    "Каковы основные компоненты сверточных нейронных сетей?",
    "Какие существуют подходы к обработке текстовых данных в машинном обучении?",
    "Какие вы знаете методы для обнаружения аномалий в данных?",
    "Какие алгоритмы машинного обучения используются для задачи регрессии?",
    "Какие инструменты для визуализации данных вы можете порекомендовать?",
    "Какие библиотеки Python используются для работы с графами и сетями?",
    "Какие существуют методы для выбора гиперпараметров модели машинного обучения?",
    "Какие алгоритмы используются для обработки звука в машинном обучении?",
    "Какие существуют методы для определения тональности текста?"
    ]
    
    
    from random import choice
    random_question = choice(questions)
    print(f"Случайный запрос нейросети:\n{random_question}")
    
    answer = formatting(ai_request(random_question, delete_commas=False))
    print(answer)
