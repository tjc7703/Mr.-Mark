from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from datetime import datetime

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
    """실시간 마케팅 뉴스 피드"""
    news_data = [
        {
            "id": 1,
            "title": "2024년 디지털 마케팅 트렌드: AI와 개인화가 주도",
            "summary": "AI 기반 개인화 마케팅이 2024년의 핵심 트렌드로 부상하고 있습니다.",
            "source": "마케팅 인사이트",
            "url": "https://www.marketinginsight.co.kr/2024-digital-marketing-trends",
            "published_at": "2024-01-15T10:30:00Z",
            "category": "트렌드"
        },
        {
            "id": 2,
            "title": "소셜미디어 마케팅 성공 사례: 인스타그램 릴스 활용법",
            "summary": "인스타그램 릴스를 활용한 브랜드 마케팅 성공 사례를 소개합니다.",
            "source": "소셜마케팅 뉴스",
            "url": "https://socialmarketing.news/instagram-reels-success-cases",
            "published_at": "2024-01-15T09:15:00Z",
            "category": "소셜미디어"
        },
        {
            "id": 3,
            "title": "바이럴 마케팅 전략: 틱톡 챌린지 활용 가이드",
            "summary": "틱톡 챌린지를 활용한 바이럴 마케팅 전략과 실행 방법을 알아봅니다.",
            "source": "바이럴 마케팅 가이드",
            "url": "https://viralmarketing.guide/tiktok-challenge-strategy",
            "published_at": "2024-01-15T08:45:00Z",
            "category": "바이럴마케팅"
        },
        {
            "id": 4,
            "title": "콘텐츠 마케팅 ROI 측정 방법론",
            "summary": "콘텐츠 마케팅의 투자 대비 수익률을 정확히 측정하는 방법을 제시합니다.",
            "source": "콘텐츠 마케팅 연구소",
            "url": "https://contentmarketing.lab/roi-measurement-guide",
            "published_at": "2024-01-15T07:30:00Z",
            "category": "콘텐츠마케팅"
        },
        {
            "id": 5,
            "title": "이메일 마케팅 자동화: 고객 생애주기별 전략",
            "summary": "고객의 생애주기에 따른 이메일 마케팅 자동화 전략을 구현해보세요.",
            "source": "이메일 마케팅 전문가",
            "url": "https://emailmarketing.pro/lifecycle-automation",
            "published_at": "2024-01-15T06:20:00Z",
            "category": "이메일마케팅"
        }
    ]
    return {"news": news_data}

@app.get("/trend")
def trend():
    """실시간 마케팅 트렌드"""
    trends_data = [
        {
            "keyword": "AI 마케팅 자동화",
            "volume": 8500,
            "growth": "+15%",
            "url": "https://trends.google.com/trends/explore?q=AI%20마케팅%20자동화"
        },
        {
            "keyword": "틱톡 마케팅",
            "volume": 7200,
            "growth": "+23%",
            "url": "https://trends.google.com/trends/explore?q=틱톡%20마케팅"
        },
        {
            "keyword": "바이럴 콘텐츠",
            "volume": 6800,
            "growth": "+18%",
            "url": "https://trends.google.com/trends/explore?q=바이럴%20콘텐츠"
        },
        {
            "keyword": "개인화 마케팅",
            "volume": 6100,
            "growth": "+12%",
            "url": "https://trends.google.com/trends/explore?q=개인화%20마케팅"
        },
        {
            "keyword": "메타버스 마케팅",
            "volume": 5400,
            "growth": "+8%",
            "url": "https://trends.google.com/trends/explore?q=메타버스%20마케팅"
        }
    ]
    return {"trends": trends_data}

@app.get("/goal")
def goal():
    """마케팅 목표 및 체크리스트"""
    return {
        "daily_goal": "조회수 3만+ 리포스트 10+ 댓글 30+",
        "weekly_goal": "팔로워 1000명 증가",
        "monthly_goal": "브랜드 인지도 20% 향상",
        "checklist": [
            {"task": "오늘의 콘텐츠 업로드", "completed": False},
            {"task": "댓글 및 DM 응답", "completed": False},
            {"task": "경쟁사 분석", "completed": False},
            {"task": "데이터 분석 및 리포트 작성", "completed": False}
        ]
    }

@app.get("/ai/feedback")
def ai_feedback():
    """AI 마케팅 피드백"""
    return {
        "suggestions": [
            {
                "type": "콘텐츠 최적화",
                "message": "해시태그 #마케팅 #소셜미디어 #바이럴 추가 권장",
                "priority": "high"
            },
            {
                "type": "포스팅 시간",
                "message": "오후 7-9시 포스팅 시 참여도 30% 향상 예상",
                "priority": "medium"
            },
            {
                "type": "콘텐츠 유형",
                "message": "비디오 콘텐츠 비중을 60%로 증가 권장",
                "priority": "high"
            }
        ]
    }

@app.get("/pipeline/status")
def pipeline_status():
    """파이프라인 상태"""
    return {
        "pipelines": [
            {
                "name": "SNS 데이터 수집",
                "status": "completed",
                "lastRun": "2024-01-15T10:30:00Z",
                "duration": 120,
                "recordsProcessed": 1500
            },
            {
                "name": "데이터 정제",
                "status": "running",
                "lastRun": "2024-01-15T10:35:00Z",
                "duration": 45,
                "recordsProcessed": 1200
            },
            {
                "name": "AI 모델 학습",
                "status": "completed",
                "lastRun": "2024-01-15T09:00:00Z",
                "duration": 1800,
                "recordsProcessed": 800
            },
            {
                "name": "품질 검증",
                "status": "completed",
                "lastRun": "2024-01-15T10:40:00Z",
                "duration": 30,
                "recordsProcessed": 1200
            },
            {
                "name": "데이터 마트 구축",
                "status": "idle",
                "lastRun": "2024-01-15T09:30:00Z",
                "duration": 300,
                "recordsProcessed": 800
            }
        ]
    }

@app.get("/quality/metrics")
def quality_metrics():
    """품질 메트릭"""
    return {
        "metrics": [
            {
                "name": "완성도",
                "value": 0.95,
                "threshold": 0.9,
                "status": "good"
            },
            {
                "name": "정확도",
                "value": 0.88,
                "threshold": 0.9,
                "status": "warning"
            },
            {
                "name": "일관성",
                "value": 0.92,
                "threshold": 0.85,
                "status": "good"
            },
            {
                "name": "최신성",
                "value": 0.78,
                "threshold": 0.8,
                "status": "warning"
            },
            {
                "name": "유효성",
                "value": 0.96,
                "threshold": 0.95,
                "status": "good"
            },
            {
                "name": "고유성",
                "value": 0.98,
                "threshold": 0.98,
                "status": "good"
            }
        ]
    }

@app.get("/ai/performance")
def ai_performance():
    """AI 모델 성능"""
    return {
        "models": [
            {
                "name": "참여율 예측",
                "accuracy": 0.85,
                "precision": 0.82,
                "recall": 0.88,
                "f1Score": 0.85,
                "lastTrained": "2024-01-15T09:00:00Z"
            },
            {
                "name": "트렌드 예측",
                "accuracy": 0.78,
                "precision": 0.75,
                "recall": 0.80,
                "f1Score": 0.77,
                "lastTrained": "2024-01-15T08:30:00Z"
            },
            {
                "name": "콘텐츠 감정 분석",
                "accuracy": 0.82,
                "precision": 0.80,
                "recall": 0.85,
                "f1Score": 0.82,
                "lastTrained": "2024-01-15T08:00:00Z"
            },
            {
                "name": "사용자 클러스터링",
                "accuracy": 0.91,
                "precision": 0.89,
                "recall": 0.93,
                "f1Score": 0.91,
                "lastTrained": "2024-01-15T07:30:00Z"
            }
        ]
    }

@app.get("/quality/issues")
def quality_issues():
    """품질 이슈"""
    return {
        "issues": [
            {
                "severity": "medium",
                "category": "posts_accuracy",
                "description": "posts 테이블의 정확도가 임계값 미달",
                "affectedRecords": 150,
                "recommendation": "데이터 형식 검증 강화 필요"
            },
            {
                "severity": "low",
                "category": "users_timeliness",
                "description": "users 테이블의 데이터가 10분 이상 지연",
                "affectedRecords": 50,
                "recommendation": "데이터 수집 주기 단축 고려"
            },
            {
                "severity": "high",
                "category": "hashtags_completeness",
                "description": "hashtags 테이블의 완성도가 임계값 미달",
                "affectedRecords": 300,
                "recommendation": "해시태그 추출 로직 개선 필요"
            }
        ]
    } 