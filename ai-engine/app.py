from fastapi import FastAPI

app = FastAPI()


@app.get("/predict/trend")
def predict_trend():
    return {"prediction": ["내일의 트렌드: AI 마케팅", "SNS 챌린지"]}


@app.get("/feedback")
def feedback():
    return {"feedback": "콘텐츠 업로드 빈도를 높이면 참여율이 증가합니다."}
