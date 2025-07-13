from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import random
from datetime import datetime, timedelta
import asyncio
from feedback_api import router as feedback_router
from abtest import router as abtest_router

app = FastAPI(title="Mr. Mark API", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터 모델
class TrendData(BaseModel):
    name: str
    value: int
    change: float

class NewsItem(BaseModel):
    title: str
    content: str
    source: str
    timestamp: str

class AIFeedback(BaseModel):
    feedback: str
    score: float
    suggestions: List[str]

# 시뮬레이션 데이터
TREND_KEYWORDS = [
    "인스타그램 릴스", "틱톡 마케팅", "AI 마케팅", "메타버스 광고", 
    "인플루언서 마케팅", "바이럴 마케팅", "데이터 기반 마케팅", "퍼스널 브랜딩"
]

NEWS_SOURCES = [
    "마케팅 인사이트", "디지털 마케팅 뉴스", "브랜드 스토리", "마케팅 트렌드"
]

app.include_router(feedback_router)
app.include_router(abtest_router)

@app.get("/")
def root():
    return {"msg": "Mr. Mark Backend API", "version": "1.0.0"}

@app.get("/feed/today")
async def get_today_feed():
    """오늘의 마케팅 소식 피드"""
    news_items = [
        {
            "title": "2024년 인스타그램 알고리즘 변화, 릴스 중심으로 전환",
            "content": "인스타그램이 릴스 콘텐츠를 우선적으로 노출하는 새로운 알고리즘을 도입했습니다.",
            "source": "마케팅 인사이트",
            "timestamp": datetime.now().isoformat()
        },
        {
            "title": "AI 기반 마케팅 자동화 도구들의 성장세",
            "content": "ChatGPT와 같은 AI 도구들이 마케팅 콘텐츠 제작에 혁신을 가져오고 있습니다.",
            "source": "디지털 마케팅 뉴스",
            "timestamp": datetime.now().isoformat()
        },
        {
            "title": "Z세대를 타겟팅한 새로운 마케팅 전략",
            "content": "진정성과 개성이 중요한 Z세대를 위한 마케팅 접근법이 주목받고 있습니다.",
            "source": "브랜드 스토리",
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    return {
        "news": [item["title"] for item in news_items],
        "detailed_news": news_items,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/trend")
async def get_trends():
    """실시간 트렌드 데이터"""
    trends = []
    for i, keyword in enumerate(TREND_KEYWORDS[:6]):
        trends.append({
            "name": keyword,
            "value": random.randint(1000, 50000),
            "change": random.uniform(-15.0, 25.0)
        })
    
    return {
        "trends": [trend["name"] for trend in trends],
        "detailed_trends": trends,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/feedback")
async def get_ai_feedback():
    """AI 피드백 시스템"""
    feedback_options = [
        {
            "feedback": "오늘의 릴스 퀄리티가 매우 좋습니다! 해시태그 최적화로 더 많은 도달을 얻을 수 있을 것 같아요.",
            "score": 8.5,
            "suggestions": ["트렌딩 해시태그 활용", "첫 3초 훅 강화", "CTA 버튼 추가"]
        },
        {
            "feedback": "콘텐츠는 좋지만 타이밍이 아쉽습니다. 저녁 7-9시 업로드가 더 효과적일 것 같아요.",
            "score": 7.2,
            "suggestions": ["업로드 시간 조정", "스토리와 연계", "인터랙션 유도"]
        },
        {
            "feedback": "브랜드 일관성이 뛰어납니다! 다음 단계로 고객 후기 콘텐츠를 추가해보세요.",
            "score": 9.1,
            "suggestions": ["고객 후기 수집", "UGC 콘텐츠 활용", "커뮤니티 구축"]
        }
    ]
    
    selected_feedback = random.choice(feedback_options)
    
    return {
        "feedback": selected_feedback["feedback"],
        "score": selected_feedback["score"],
        "suggestions": selected_feedback["suggestions"],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/sns/collect")
async def collect_sns_data():
    """SNS 데이터 수집 API"""
    # 실제로는 data/pipelines/collect_sns_data.py와 연동
    return {
        "status": "success",
        "collected_data": {
            "twitter": random.randint(100, 1000),
            "instagram": random.randint(500, 2000),
            "linkedin": random.randint(50, 300),
            "youtube": random.randint(200, 800)
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/data/quality")
async def check_data_quality():
    """데이터 품질 검증 API"""
    # 실제로는 data/pipelines/quality_checks.py와 연동
    return {
        "status": "success",
        "quality_score": random.uniform(85.0, 98.0),
        "issues_found": random.randint(0, 5),
        "recommendations": [
            "중복 데이터 정리 필요",
            "누락된 해시태그 보완",
            "이미지 품질 개선"
        ],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/ai/preprocess")
async def preprocess_text():
    """텍스트 전처리 API"""
    # 실제로는 ai-engine/preprocessing/text_processor.py와 연동
    return {
        "status": "success",
        "processed_texts": random.randint(100, 500),
        "cleaned_data": random.randint(80, 95),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/ai/train")
async def train_models():
    """AI 모델 훈련 API"""
    # 실제로는 ai-engine/training/model_trainer.py와 연동
    return {
        "status": "success",
        "models_trained": ["trend_predictor", "sentiment_analyzer", "content_classifier"],
        "accuracy": {
            "trend_predictor": random.uniform(0.75, 0.92),
            "sentiment_analyzer": random.uniform(0.80, 0.95),
            "content_classifier": random.uniform(0.85, 0.98)
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "running",
            "database": "connected",
            "ai_engine": "ready"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
