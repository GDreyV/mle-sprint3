# импортируем библиотеку для работы со случайными числами
import random

# импортируем класс для создания экземпляра FastAPI-приложения
from fastapi import FastAPI
from fast_api_handler import FastApiHandler

# создаём экземпляр FastAPI-приложения
app = FastAPI()

handler = FastApiHandler()

# обрабатываем запросы к корню приложения
@app.get("/")
def read_root():
    return {"Hello": "World"}


# обрабатываем запросы к специальному пути для получения предсказания модели
# временно имитируем предсказание со случайной генерацией score
@app.get("/api/churn/{user_id}")
def get_prediction_for_item(user_id: str):
    response = {
        "user_id": user_id, 
        "probability": probability, 
        "is_churn": int(probability > 0.5)
    } 
    return response


@app.post("/api/credit/{client_id}")
def is_credit_approved(client_id: str, model_params: dict):
    all_params = {
        "client_id": client_id,
        "model_params": model_params
    }
    user_prediction = handler.handle(all_params)
    score = user_prediction["predicted_credit_rating"]
    return {"client_id": client_id, "approved": 1 if score > 600 else 0}


@app.get("/service-status")
def health_check():
    return {"status": "ok"}
