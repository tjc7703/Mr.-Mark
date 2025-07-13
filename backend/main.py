from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"msg": "Mr. Mark Backend API"}

@app.get("/feed/today")
def today_feed():
    return {"news": ["실시간 마케팅 뉴스 예시", "트렌드 소식 예시"]}

@app.get("/trend")
def trend():
    return {"trends": ["SNS 마케팅", "AI 자동화", "바이럴 캠페인"]}

@app.get("/goal")
def goal():
    return {"goal": "조회수 3만+ 리포스트 10+ 댓글 30+"} 