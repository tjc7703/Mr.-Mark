from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import random
from datetime import datetime, timedelta
import asyncio
from feedback_api import router as feedback_router
from abtest import router as abtest_router
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Mr. Mark Backend API", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    "인스타그램 릴스",
    "틱톡 마케팅",
    "AI 마케팅",
    "메타버스 광고",
    "인플루언서 마케팅",
    "바이럴 마케팅",
    "데이터 기반 마케팅",
    "퍼스널 브랜딩",
]

NEWS_SOURCES = [
    "마케팅 인사이트",
    "디지털 마케팅 뉴스",
    "브랜드 스토리",
    "마케팅 트렌드",
]

app.include_router(feedback_router)
app.include_router(abtest_router)


@app.get("/")
def read_root():
    return {"msg": "Mr. Mark Backend API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    """헬스체크 엔드포인트"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/api/backend/health")
def kong_health_check():
    """Kong 경유 헬스체크 엔드포인트"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/metrics")
def metrics():
    """메트릭 엔드포인트"""
    return {
        "requests_total": 0,
        "requests_success": 0,
        "requests_error": 0,
        "uptime_seconds": 0
    }


@app.get("/feed/today")
def today_feed():
    """실시간 마케팅 뉴스 피드"""
    try:
        news_data = [
            {
                "id": 1,
                "title": "2024년 디지털 마케팅 트렌드: AI와 개인화가 주도",
                "summary": "AI 기반 개인화 마케팅이 2024년의 핵심 트렌드로 부상하고 있습니다.",
                "source": "마케팅 인사이트",
                "url": "https://www.marketinginsight.co.kr/2024-digital-marketing-trends",
                "published_at": "2024-01-15T10:30:00Z",
                "category": "트렌드",
            },
            {
                "id": 2,
                "title": "소셜미디어 마케팅 성공 사례: 인스타그램 릴스 활용법",
                "summary": "인스타그램 릴스를 활용한 브랜드 마케팅 성공 사례를 소개합니다.",
                "source": "소셜마케팅 뉴스",
                "url": "https://socialmarketing.news/instagram-reels-success-cases",
                "published_at": "2024-01-15T09:15:00Z",
                "category": "소셜미디어",
            },
            {
                "id": 3,
                "title": "바이럴 마케팅 전략: 틱톡 챌린지 활용 가이드",
                "summary": "틱톡 챌린지를 활용한 바이럴 마케팅 전략과 실행 방법을 알아봅니다.",
                "source": "바이럴 마케팅 가이드",
                "url": "https://viralmarketing.guide/tiktok-challenge-strategy",
                "published_at": "2024-01-15T08:45:00Z",
                "category": "바이럴마케팅",
            },
            {
                "id": 4,
                "title": "콘텐츠 마케팅 ROI 측정 방법론",
                "summary": "콘텐츠 마케팅의 투자 대비 수익률을 정확히 측정하는 방법을 제시합니다.",
                "source": "콘텐츠 마케팅 연구소",
                "url": "https://contentmarketing.lab/roi-measurement-guide",
                "published_at": "2024-01-15T07:30:00Z",
                "category": "콘텐츠마케팅",
            },
            {
                "id": 5,
                "title": "이메일 마케팅 자동화: 고객 생애주기별 전략",
                "summary": "고객의 생애주기에 따른 이메일 마케팅 자동화 전략을 구현해보세요.",
                "source": "이메일 마케팅 전문가",
                "url": "https://emailmarketing.pro/lifecycle-automation",
                "published_at": "2024-01-15T06:20:00Z",
                "category": "이메일마케팅",
            },
        ]
        logger.info(f"피드 데이터 조회 성공: {len(news_data)}개 항목")
        return {"news": news_data}
    except Exception as e:
        logger.error(f"피드 데이터 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="피드 데이터를 불러오는데 실패했습니다.")


@app.get("/trend")
def trend():
    """실시간 마케팅 트렌드"""
    try:
        trends_data = [
            {
                "keyword": "AI 마케팅 자동화",
                "volume": 8500,
                "growth": "+15%",
                "url": "https://trends.google.com/trends/explore?q=AI%20마케팅%20자동화",
            },
            {
                "keyword": "틱톡 마케팅",
                "volume": 7200,
                "growth": "+23%",
                "url": "https://trends.google.com/trends/explore?q=틱톡%20마케팅",
            },
            {
                "keyword": "바이럴 콘텐츠",
                "volume": 6800,
                "growth": "+18%",
                "url": "https://trends.google.com/trends/explore?q=바이럴%20콘텐츠",
            },
            {
                "keyword": "개인화 마케팅",
                "volume": 6100,
                "growth": "+12%",
                "url": "https://trends.google.com/trends/explore?q=개인화%20마케팅",
            },
            {
                "keyword": "메타버스 마케팅",
                "volume": 5400,
                "growth": "+8%",
                "url": "https://trends.google.com/trends/explore?q=메타버스%20마케팅",
            },
        ]
        logger.info(f"트렌드 데이터 조회 성공: {len(trends_data)}개 항목")
        return {"trends": trends_data}
    except Exception as e:
        logger.error(f"트렌드 데이터 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="트렌드 데이터를 불러오는데 실패했습니다.")


@app.get("/goal")
def goal():
    """마케팅 목표 및 체크리스트"""
    try:
        return {
            "daily_goal": "조회수 3만+ 리포스트 10+ 댓글 30+",
            "weekly_goal": "팔로워 1000명 증가",
            "monthly_goal": "브랜드 인지도 20% 향상",
            "checklist": [
                {"task": "오늘의 콘텐츠 업로드", "completed": False},
                {"task": "댓글 및 DM 응답", "completed": False},
                {"task": "경쟁사 분석", "completed": False},
                {"task": "데이터 분석 및 리포트 작성", "completed": False},
            ],
        }
    except Exception as e:
        logger.error(f"목표 데이터 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="목표 데이터를 불러오는데 실패했습니다.")


@app.get("/ai/feedback")
def ai_feedback():
    """AI 마케팅 피드백"""
    try:
        return {
            "suggestions": [
                {
                    "type": "콘텐츠 최적화",
                    "message": "해시태그 #마케팅 #소셜미디어 #바이럴 추가 권장",
                    "priority": "high",
                },
                {
                    "type": "포스팅 시간",
                    "message": "오후 7-9시 포스팅 시 참여도 30% 향상 예상",
                    "priority": "medium",
                },
                {
                    "type": "콘텐츠 유형",
                    "message": "비디오 콘텐츠 비중을 60%로 증가 권장",
                    "priority": "high",
                },
            ]
        }
    except Exception as e:
        logger.error(f"AI 피드백 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="AI 피드백을 불러오는데 실패했습니다.")


@app.get("/pipeline/status")
def pipeline_status():
    """파이프라인 상태"""
    try:
        return {
            "pipelines": [
                {
                    "name": "SNS 데이터 수집",
                    "status": "completed",
                    "lastRun": "2024-01-15T10:30:00Z",
                    "duration": 120,
                    "recordsProcessed": 1500,
                },
                {
                    "name": "데이터 정제",
                    "status": "running",
                    "lastRun": "2024-01-15T10:35:00Z",
                    "duration": 45,
                    "recordsProcessed": 1200,
                },
                {
                    "name": "AI 모델 학습",
                    "status": "completed",
                    "lastRun": "2024-01-15T09:00:00Z",
                    "duration": 1800,
                    "recordsProcessed": 800,
                },
                {
                    "name": "품질 검증",
                    "status": "completed",
                    "lastRun": "2024-01-15T10:40:00Z",
                    "duration": 30,
                    "recordsProcessed": 1200,
                },
                {
                    "name": "데이터 마트 구축",
                    "status": "idle",
                    "lastRun": "2024-01-15T09:30:00Z",
                    "duration": 300,
                    "recordsProcessed": 800,
                },
            ]
        }
    except Exception as e:
        logger.error(f"파이프라인 상태 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="파이프라인 상태를 불러오는데 실패했습니다.")


@app.get("/quality/metrics")
def quality_metrics():
    """품질 메트릭"""
    try:
        return {
            "data_quality_score": 95.2,
            "model_accuracy": 87.8,
            "system_uptime": 99.9,
            "response_time_avg": 245,
            "error_rate": 0.1,
            "user_satisfaction": 4.6,
        }
    except Exception as e:
        logger.error(f"품질 메트릭 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="품질 메트릭을 불러오는데 실패했습니다.")


@app.get("/ai/performance")
def ai_performance():
    """AI 성능 지표"""
    try:
        return {
            "model_performance": {
                "accuracy": 0.92,
                "precision": 0.89,
                "recall": 0.91,
                "f1_score": 0.90,
            },
            "inference_time": 0.15,
            "training_time": 1800,
            "last_updated": "2024-01-15T10:00:00Z",
        }
    except Exception as e:
        logger.error(f"AI 성능 지표 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="AI 성능 지표를 불러오는데 실패했습니다.")


@app.get("/quality/issues")
def quality_issues():
    """품질 이슈"""
    try:
        return {
            "issues": [
                {
                    "id": 1,
                    "type": "data_quality",
                    "severity": "medium",
                    "description": "일부 SNS 데이터 누락",
                    "status": "in_progress",
                    "created_at": "2024-01-15T09:30:00Z",
                },
                {
                    "id": 2,
                    "type": "model_performance",
                    "severity": "low",
                    "description": "트렌드 예측 정확도 개선 필요",
                    "status": "resolved",
                    "created_at": "2024-01-15T08:15:00Z",
                },
            ]
        }
    except Exception as e:
        logger.error(f"품질 이슈 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="품질 이슈를 불러오는데 실패했습니다.")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """전역 예외 처리"""
    logger.error(f"예상치 못한 오류 발생: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "서버 내부 오류가 발생했습니다."}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
