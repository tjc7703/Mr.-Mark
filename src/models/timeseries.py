from .base_model import BaseModel
from prophet import Prophet


class TimeSeriesModel(BaseModel):
    def __init__(self):
        self.model = Prophet()

    def train(self, df):
        # df: pandas DataFrame with columns ['ds', 'y']
        self.model.fit(df)

    def predict(self, future):
        # future: pandas DataFrame with column ['ds']
        return self.model.predict(future)

    def evaluate(self, df):
        # df: pandas DataFrame with columns ['ds', 'y']
        forecast = self.model.predict(df)
        # 예시: MSE 계산
        from sklearn.metrics import mean_squared_error

        return mean_squared_error(df["y"], forecast["yhat"])
