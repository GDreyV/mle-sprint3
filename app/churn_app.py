"""FastAPI-приложение для модели оттока."""

from fastapi import FastAPI, Body
from fast_api_handler import FastApiHandler

"""
Пример запуска из директории mle-sprint3/app:
uvicorn churn_app:app --reload --port 8081 --host 0.0.0.0

Для просмотра документации API и совершения тестовых запросов зайти на http://127.0.0.1:8081/docs

Если используется другой порт, то заменить 8081 на этот порт
"""

# создаём FastAPI-приложение 
app = FastAPI()

# создаём обработчик запросов для API
handler = FastApiHandler()

# ваш код функции-обработчика get_prediction_for_item здесь

@app.post("/api/churn")
def get_prediction_for_item(user_id: str, model_params: dict) -> dict:
    payload = {
        "user_id": user_id,
        "model_params": model_params
    }
    score = handler.handle(payload)
    response = {
        "user_id": user_id,  # тот, что приходит в запросе
        "probability": score,  # значение вероятности оттока
        "is_churn": 1 if score > 0.5 else 0  # 1, если отток, иначе 0
    }
    return response
