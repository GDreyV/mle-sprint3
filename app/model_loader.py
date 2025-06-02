from typing import cast
from catboost import CatBoostClassifier
# импортируйте необходимую библиотеку
# ваш код здесь


def load_churn_model(model_path: str) -> CatBoostClassifier | None:
    """Загружаем обученную модель оттока.
    Args:
        model_path (str): Путь до модели.
    """
    model = None
    try:
        model = CatBoostClassifier()
        model.load_model(model_path)
        print("Model loaded successfully")
    except Exception as e:
        print(f"Failed to load model: {e}")
    return model


class FastApiHandler:
    """Класс FastApiHandler, который обрабатывает запрос и возвращает предсказание."""

    def __init__(self):
        """Инициализация переменных класса."""

        # типы параметров запроса для проверки
        self.param_types = {
            "user_id": str,
            "model_params": dict
        }

        self.model_path = "models/catboost_churn_model.bin"
        model = load_churn_model(model_path=self.model_path)
        if not model:
            raise ValueError(f"Model not loaded from {self.model_path}")
        
        # необходимые параметры для предсказаний модели оттока
        self.required_model_params = set(cast(list[str], model.feature_names_))

    def load_churn_model(self, model_path: str):
        """Загружаем обученную модель оттока.
        Args:
            model_path (str): Путь до модели.
        """
        try:
            self.model = CatBoostClassifier()
            self.model.load_model(model_path)
        except Exception as e:
            print(f"Failed to load model: {e}")

    def churn_predict(self, model_params: dict) -> float:
        """Предсказываем вероятность оттока.

        Args:
            model_params (dict): Параметры для модели.

        Returns:
            float - вероятность оттока от 0 до 1
        """
        param_values_list = list(model_params.values())
        return self.model.predict_proba(param_values_list)[1]
        
    def check_required_query_params(self, query_params: dict) -> bool:
        """
        Проверяем параметры запроса на наличие обязательного набора параметров.
        """

        if "user_id" not in query_params or "model_params" not in query_params:
            return False

        if not isinstance(query_params["user_id"], self.param_types["user_id"]):
            return False

        if not isinstance(query_params["model_params"], self.param_types["model_params"]):
            return False

        return True
    
    def check_required_model_params(self, model_params: dict) -> bool:
        """Проверяем параметры пользователя на наличие обязательного набора.
        
        Args:
        model_params (dict): Параметры пользователя для предсказания.
        
        Returns:
        bool: True - если есть нужные параметры, False - иначе
        """
        params_set = set(model_params.keys())
        if set(model_params.keys()) == set(self.required_model_params):
            return True
        
        print(self.required_model_params.difference(params_set))
        return False
    
    def validate_params(self, params: dict) -> bool:
        """Разбираем запрос и проверяем его корректность.
        
        Args:
        params (dict): Словарь параметров запроса.
        
        Returns:
        - **dict**: Cловарь со всеми параметрами запроса.
        """
        if self.check_required_query_params(params):
            print("All query params exist")
        else:
            print("Not all query params exist")
            return False
        
        if self.check_required_model_params(params["model_params"]):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False
        return True
            
    def handle(self, params):
        """Функция для обработки запросов API параметров входящего запроса.

        Args:
            params (dict): Словарь параметров запроса.

        Returns:
            dict: Словарь, содержащий результат выполнения запроса.
        """
        try:
            # Валидируем запрос к API
            if not self.validate_params(params):
                response = {'Error': 'Problem with parameters'}
            else:
                model_params = params['model_params']
                user_id = params['user_id']
                probability = self.churn_predict(model_params)
                response = {'user_id': user_id, 'probability': probability, 'is_churn': int(probability > 0.5)}
        except Exception as e:
            print(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}
        else:
            return response


if __name__ == "__main__":
    model_path = "models/catboost_credit_model.bin"
    if model := load_churn_model(model_path='models/catboost_churn_model.bin'):
        print(f"Model parameter names: {model.get_all_params()}")
        print(f'Model parameter names: {model.feature_names_}')