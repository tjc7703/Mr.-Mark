from .base_model import BaseModel
from transformers import pipeline


class TextClassificationModel(BaseModel):
    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        self.model = pipeline("sentiment-analysis", model=model_name)

    def train(self, X, y=None):
        # transformers pipeline은 사전학습 모델 사용, 별도 학습 생략
        pass

    def predict(self, X):
        return self.model(X)

    def evaluate(self, X, y):
        # 간단 예시: 예측값과 y 비교하여 정확도 계산
        preds = [1 if r["label"] == "POSITIVE" else 0 for r in self.model(X)]
        return sum([p == t for p, t in zip(preds, y)]) / len(y)
