from classification import ClassificationModel
from regression import RegressionModel
from timeseries import TimeSeriesModel
from text_classification import TextClassificationModel
import numpy as np
import pandas as pd

# 분류 예시
X_cls = np.random.rand(100, 4)
y_cls = np.random.randint(0, 2, 100)
cls_model = ClassificationModel()
cls_model.train(X_cls, y_cls)
print('Classification acc:', cls_model.evaluate(X_cls, y_cls))

# 회귀 예시
X_reg = np.random.rand(100, 3)
y_reg = np.random.rand(100)
reg_model = RegressionModel()
reg_model.train(X_reg, y_reg)
print('Regression MSE:', reg_model.evaluate(X_reg, y_reg))

# 시계열 예시
future = pd.DataFrame({'ds': pd.date_range('2024-01-01', periods=10)})
df_ts = pd.DataFrame({'ds': pd.date_range('2024-01-01', periods=10), 'y': np.random.rand(10)})
ts_model = TimeSeriesModel()
ts_model.train(df_ts)
print('TimeSeries MSE:', ts_model.evaluate(df_ts))

# 텍스트 분류 예시
texts = ["I love this!", "I hate this!"]
y_text = [1, 0]
txt_model = TextClassificationModel()
print('TextClassification acc:', txt_model.evaluate(texts, y_text)) 