from fastapi import FastAPI

app = FastAPI()

@app.get("/predict")
def predict():
    return {"prediction": "AI 기반 마케팅 트렌드 예측" }
