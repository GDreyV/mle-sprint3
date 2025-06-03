# импортируем библиотеку для работы со случайными числами
import random

# импортируем класс для создания экземпляра FastAPI-приложения
from fastapi import FastAPI
from fast_api_handler import FastApiHandler
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Histogram, Counter

# создаём экземпляр FastAPI-приложения
app = FastAPI()

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

handler = FastApiHandler()

# обрабатываем запросы к корню приложения
@app.get("/")
def read_root():
    return {"Hello": "World"}


# main_app_predictions — объект метрики
main_app_predictions = Histogram(
    # имя метрики
    "main_app_predictions",
    # описание метрики
    "Histogram of predictions",
    # указываем корзины для гистограммы
    buckets=(1, 2, 4, 5, 10)
) 
main_app_positive_predictions = Counter('main_app_positive_predictions', 'Number of positive predictions')

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
    score: float = user_prediction["predicted_credit_rating"]
    main_app_predictions.observe(score)
    if score > 600:
        main_app_positive_predictions.inc()
    return {"client_id": client_id, "approved": 1 if score > 600 else 0}


@app.get("/service-status")
def health_check():
    return {"status": "ok"}
