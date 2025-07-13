from .base_model import BaseModel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


class ClassificationModel(BaseModel):
    def __init__(self):
        self.model = LogisticRegression()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def evaluate(self, X, y):
        preds = self.predict(X)
        return accuracy_score(y, preds)
