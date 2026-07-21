import joblib
from app.config import Config


class ModelLoader:

    def __init__(self):
        self.model = joblib.load(Config.MODEL_PATH)

    def get_model(self):
        return self.model