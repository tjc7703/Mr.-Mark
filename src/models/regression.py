from .base_model import BaseModel
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

class RegressionModel(BaseModel):
    def __init__(self):
        self.model = LinearRegression()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def evaluate(self, X, y):
        preds = self.predict(X)
        return mean_squared_error(y, preds) 