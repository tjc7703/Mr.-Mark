#!/usr/bin/env python3
"""
AI 학습/예측 파이프라인
Scikit-learn, Prophet, HuggingFace를 활용한 마케팅 AI 분석
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
import numpy as np
from pathlib import Path
import pickle
import joblib
from dataclasses import dataclass
import asyncio
import sqlite3
import os

# AI/ML 라이브러리
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import warnings

warnings.filterwarnings("ignore")

# Prophet (시계열 예측)
try:
    from prophet import Prophet

    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    print("Prophet not available. Install with: pip install prophet")

# HuggingFace (NLP)
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    from transformers import TextClassificationPipeline

    HUGGINGFACE_AVAILABLE = True
except ImportError:
    HUGGINGFACE_AVAILABLE = False
    print("HuggingFace not available. Install with: pip install transformers torch")

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AIModel:
    """AI 모델 정의"""

    name: str
    model_type: str
    description: str
    features: List[str]
    target: str
    hyperparameters: Dict[str, Any]


class AIPipeline:
    """AI 학습/예측 파이프라인"""

    def __init__(self):
        self.models_path = Path("data/models")
        self.models_path.mkdir(parents=True, exist_ok=True)

        self.warehouse_path = Path("data/warehouse/warehouse.db")
        self.models = self._define_models()
        self.scalers = {}
        self.label_encoders = {}

    def _define_models(self) -> Dict[str, AIModel]:
        """AI 모델 정의"""
        return {
            "engagement_prediction": AIModel(
                name="engagement_prediction",
                model_type="regression",
                description="포스트 참여율 예측",
                features=[
                    "likes",
                    "comments",
                    "shares",
                    "hashtag_count",
                    "content_length",
                    "hour_of_day",
                ],
                target="engagement_rate",
                hyperparameters={"n_estimators": 100, "max_depth": 10},
            ),
            "trend_forecasting": AIModel(
                name="trend_forecasting",
                model_type="time_series",
                description="트렌드 시계열 예측",
                features=["date", "trend_score", "volume"],
                target="trend_score",
                hyperparameters={
                    "changepoint_prior_scale": 0.05,
                    "seasonality_prior_scale": 10,
                },
            ),
            "content_sentiment": AIModel(
                name="content_sentiment",
                model_type="nlp",
                description="콘텐츠 감정 분석",
                features=["content"],
                target="sentiment_score",
                hyperparameters={
                    "model_name": "cardiffnlp/twitter-roberta-base-sentiment-latest"
                },
            ),
            "user_clustering": AIModel(
                name="user_clustering",
                model_type="clustering",
                description="사용자 세분화",
                features=[
                    "post_count",
                    "avg_engagement_rate",
                    "followers",
                    "following",
                ],
                target="cluster",
                hyperparameters={"n_clusters": 5},
            ),
            "optimal_posting_time": AIModel(
                name="optimal_posting_time",
                model_type="classification",
                description="최적 포스팅 시간 예측",
                features=["hour", "day_of_week", "content_type", "hashtag_count"],
                target="high_engagement",
                hyperparameters={"n_estimators": 100, "max_depth": 8},
            ),
        }

    async def load_data(self) -> Dict[str, pd.DataFrame]:
        """웨어하우스에서 데이터 로드"""
        try:
            conn = sqlite3.connect(self.warehouse_path)

            # 각 모델별 데이터 로드
            data = {}

            # 참여율 예측용 데이터
            engagement_query = """
                SELECT 
                    likes, comments, shares,
                    LENGTH(hashtags) as hashtag_count,
                    LENGTH(content) as content_length,
                    CAST(strftime('%H', created_at) AS INTEGER) as hour_of_day,
                    (likes + comments + shares) / 1000.0 as engagement_rate
                FROM posts 
                WHERE likes > 0 OR comments > 0 OR shares > 0
            """
            data["engagement_prediction"] = pd.read_sql_query(engagement_query, conn)

            # 트렌드 예측용 데이터
            trend_query = """
                SELECT 
                    date,
                    trend_score,
                    volume
                FROM trends 
                WHERE trend_score > 0
                ORDER BY date
            """
            data["trend_forecasting"] = pd.read_sql_query(trend_query, conn)

            # 사용자 클러스터링용 데이터
            user_query = """
                SELECT 
                    post_count,
                    avg_engagement_rate,
                    followers,
                    following
                FROM users 
                WHERE followers > 0
            """
            data["user_clustering"] = pd.read_sql_query(user_query, conn)

            # 최적 포스팅 시간용 데이터
            posting_time_query = """
                SELECT 
                    CAST(strftime('%H', created_at) AS INTEGER) as hour,
                    CAST(strftime('%w', created_at) AS INTEGER) as day_of_week,
                    media_type as content_type,
                    LENGTH(hashtags) as hashtag_count,
                    CASE WHEN (likes + comments + shares) > 100 THEN 1 ELSE 0 END as high_engagement
                FROM posts 
                WHERE likes > 0 OR comments > 0 OR shares > 0
            """
            data["optimal_posting_time"] = pd.read_sql_query(posting_time_query, conn)

            # 콘텐츠 감정 분석용 데이터
            content_query = """
                SELECT content
                FROM posts 
                WHERE content IS NOT NULL AND content != ''
                LIMIT 1000
            """
            data["content_sentiment"] = pd.read_sql_query(content_query, conn)

            conn.close()
            logger.info("데이터 로드 완료")
            return data

        except Exception as e:
            logger.error(f"데이터 로드 실패: {str(e)}")
            return {}

    async def train_models(self, data: Dict[str, pd.DataFrame]):
        """모든 AI 모델 학습"""
        try:
            logger.info("AI 모델 학습 시작")

            for model_name, model_config in self.models.items():
                if model_name in data and not data[model_name].empty:
                    await self._train_model(model_name, model_config, data[model_name])

            logger.info("AI 모델 학습 완료")

        except Exception as e:
            logger.error(f"모델 학습 실패: {str(e)}")

    async def _train_model(
        self, model_name: str, model_config: AIModel, data: pd.DataFrame
    ):
        """개별 모델 학습"""
        try:
            logger.info(f"모델 학습 시작: {model_name}")

            if model_config.model_type == "regression":
                await self._train_regression_model(model_name, model_config, data)
            elif model_config.model_type == "time_series":
                await self._train_time_series_model(model_name, model_config, data)
            elif model_config.model_type == "nlp":
                await self._train_nlp_model(model_name, model_config, data)
            elif model_config.model_type == "clustering":
                await self._train_clustering_model(model_name, model_config, data)
            elif model_config.model_type == "classification":
                await self._train_classification_model(model_name, model_config, data)

            logger.info(f"모델 학습 완료: {model_name}")

        except Exception as e:
            logger.error(f"모델 학습 실패: {model_name} - {str(e)}")

    async def _train_regression_model(
        self, model_name: str, model_config: AIModel, data: pd.DataFrame
    ):
        """회귀 모델 학습"""
        try:
            # 특성과 타겟 분리
            X = data[model_config.features].fillna(0)
            y = data[model_config.target]

            # 데이터 분할
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            # 스케일링
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)

            # 모델 학습
            model = RandomForestRegressor(
                **model_config.hyperparameters, random_state=42
            )
            model.fit(X_train_scaled, y_train)

            # 예측 및 평가
            y_pred = model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)

            # 모델 저장
            model_path = self.models_path / f"{model_name}.joblib"
            scaler_path = self.models_path / f"{model_name}_scaler.joblib"

            joblib.dump(model, model_path)
            joblib.dump(scaler, scaler_path)

            # 성능 메트릭 저장
            metrics = {
                "mse": mse,
                "r2": r2,
                "mae": mae,
                "feature_importance": dict(
                    zip(model_config.features, model.feature_importances_)
                ),
            }

            metrics_path = self.models_path / f"{model_name}_metrics.json"
            with open(metrics_path, "w") as f:
                json.dump(metrics, f, indent=2)

            logger.info(f"회귀 모델 학습 완료: {model_name} - R²: {r2:.3f}")

        except Exception as e:
            logger.error(f"회귀 모델 학습 실패: {model_name} - {str(e)}")

    async def _train_time_series_model(
        self, model_name: str, model_config: AIModel, data: pd.DataFrame
    ):
        """시계열 모델 학습 (Prophet)"""
        if not PROPHET_AVAILABLE:
            logger.warning("Prophet not available, skipping time series model")
            return

        try:
            # Prophet 형식으로 데이터 변환
            prophet_data = data.rename(columns={"date": "ds", model_config.target: "y"})
            prophet_data = prophet_data[["ds", "y"]].dropna()

            # Prophet 모델 학습
            model = Prophet(**model_config.hyperparameters)
            model.fit(prophet_data)

            # 모델 저장
            model_path = self.models_path / f"{model_name}.pkl"
            with open(model_path, "wb") as f:
                pickle.dump(model, f)

            logger.info(f"시계열 모델 학습 완료: {model_name}")

        except Exception as e:
            logger.error(f"시계열 모델 학습 실패: {model_name} - {str(e)}")

    async def _train_nlp_model(
        self, model_name: str, model_config: AIModel, data: pd.DataFrame
    ):
        """NLP 모델 학습 (HuggingFace)"""
        if not HUGGINGFACE_AVAILABLE:
            logger.warning("HuggingFace not available, skipping NLP model")
            return

        try:
            # 감정 분석 파이프라인 생성
            model_name_hf = model_config.hyperparameters.get(
                "model_name", "cardiffnlp/twitter-roberta-base-sentiment-latest"
            )

            sentiment_pipeline = pipeline(
                "sentiment-analysis", model=model_name_hf, tokenizer=model_name_hf
            )

            # 샘플 데이터로 테스트
            sample_texts = data["content"].head(10).tolist()
            results = sentiment_pipeline(sample_texts)

            # 모델 저장
            model_path = self.models_path / f"{model_name}_pipeline.joblib"
            joblib.dump(sentiment_pipeline, model_path)

            logger.info(f"NLP 모델 학습 완료: {model_name}")

        except Exception as e:
            logger.error(f"NLP 모델 학습 실패: {model_name} - {str(e)}")

    async def _train_clustering_model(
        self, model_name: str, model_config: AIModel, data: pd.DataFrame
    ):
        """클러스터링 모델 학습"""
        try:
            # 특성 선택 및 전처리
            X = data[model_config.features].fillna(0)

            # 스케일링
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            # KMeans 클러스터링
            n_clusters = model_config.hyperparameters.get("n_clusters", 5)
            model = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = model.fit_predict(X_scaled)

            # 클러스터 결과를 데이터에 추가
            data["cluster"] = clusters

            # 모델 저장
            model_path = self.models_path / f"{model_name}.joblib"
            scaler_path = self.models_path / f"{model_name}_scaler.joblib"

            joblib.dump(model, model_path)
            joblib.dump(scaler, scaler_path)

            # 클러스터 분석 결과 저장
            cluster_analysis = (
                data.groupby("cluster")[model_config.features].mean().to_dict()
            )

            analysis_path = self.models_path / f"{model_name}_analysis.json"
            with open(analysis_path, "w") as f:
                json.dump(cluster_analysis, f, indent=2)

            logger.info(
                f"클러스터링 모델 학습 완료: {model_name} - {n_clusters}개 클러스터"
            )

        except Exception as e:
            logger.error(f"클러스터링 모델 학습 실패: {model_name} - {str(e)}")

    async def _train_classification_model(
        self, model_name: str, model_config: AIModel, data: pd.DataFrame
    ):
        """분류 모델 학습"""
        try:
            # 특성과 타겟 분리
            X = data[model_config.features].fillna(0)
            y = data[model_config.target]

            # 데이터 분할
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            # 스케일링
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)

            # 모델 학습
            model = RandomForestRegressor(
                **model_config.hyperparameters, random_state=42
            )
            model.fit(X_train_scaled, y_train)

            # 예측 및 평가
            y_pred = model.predict(X_test_scaled)
            accuracy = (y_pred == y_test).mean()

            # 모델 저장
            model_path = self.models_path / f"{model_name}.joblib"
            scaler_path = self.models_path / f"{model_name}_scaler.joblib"

            joblib.dump(model, model_path)
            joblib.dump(scaler, scaler_path)

            # 성능 메트릭 저장
            metrics = {
                "accuracy": accuracy,
                "feature_importance": dict(
                    zip(model_config.features, model.feature_importances_)
                ),
            }

            metrics_path = self.models_path / f"{model_name}_metrics.json"
            with open(metrics_path, "w") as f:
                json.dump(metrics, f, indent=2)

            logger.info(f"분류 모델 학습 완료: {model_name} - 정확도: {accuracy:.3f}")

        except Exception as e:
            logger.error(f"분류 모델 학습 실패: {model_name} - {str(e)}")

    async def predict(
        self, model_name: str, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """모델 예측"""
        try:
            model_path = self.models_path / f"{model_name}.joblib"

            if not model_path.exists():
                return {"error": f"모델을 찾을 수 없습니다: {model_name}"}

            model = joblib.load(model_path)

            if model_name == "engagement_prediction":
                return await self._predict_engagement(model, input_data)
            elif model_name == "optimal_posting_time":
                return await self._predict_posting_time(model, input_data)
            elif model_name == "user_clustering":
                return await self._predict_user_cluster(model, input_data)
            else:
                return {"error": f"지원하지 않는 모델: {model_name}"}

        except Exception as e:
            logger.error(f"예측 실패: {model_name} - {str(e)}")
            return {"error": str(e)}

    async def _predict_engagement(
        self, model, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """참여율 예측"""
        try:
            # 입력 데이터 전처리
            features = [
                "likes",
                "comments",
                "shares",
                "hashtag_count",
                "content_length",
                "hour_of_day",
            ]
            X = np.array(
                [
                    [
                        input_data.get("likes", 0),
                        input_data.get("comments", 0),
                        input_data.get("shares", 0),
                        input_data.get("hashtag_count", 0),
                        input_data.get("content_length", 0),
                        input_data.get("hour_of_day", 12),
                    ]
                ]
            )

            # 스케일링
            scaler_path = self.models_path / "engagement_prediction_scaler.joblib"
            if scaler_path.exists():
                scaler = joblib.load(scaler_path)
                X_scaled = scaler.transform(X)
            else:
                X_scaled = X

            # 예측
            prediction = model.predict(X_scaled)[0]

            return {
                "predicted_engagement_rate": float(prediction),
                "confidence": 0.85,  # 예시 값
            }

        except Exception as e:
            return {"error": f"참여율 예측 실패: {str(e)}"}

    async def _predict_posting_time(
        self, model, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """최적 포스팅 시간 예측"""
        try:
            # 입력 데이터 전처리
            features = ["hour", "day_of_week", "content_type", "hashtag_count"]
            X = np.array(
                [
                    [
                        input_data.get("hour", 12),
                        input_data.get("day_of_week", 1),
                        input_data.get("content_type", 0),
                        input_data.get("hashtag_count", 0),
                    ]
                ]
            )

            # 스케일링
            scaler_path = self.models_path / "optimal_posting_time_scaler.joblib"
            if scaler_path.exists():
                scaler = joblib.load(scaler_path)
                X_scaled = scaler.transform(X)
            else:
                X_scaled = X

            # 예측
            prediction = model.predict(X_scaled)[0]

            return {
                "optimal_posting_time": int(prediction),
                "high_engagement_probability": float(prediction > 0.5),
            }

        except Exception as e:
            return {"error": f"포스팅 시간 예측 실패: {str(e)}"}

    async def _predict_user_cluster(
        self, model, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """사용자 클러스터 예측"""
        try:
            # 입력 데이터 전처리
            features = ["post_count", "avg_engagement_rate", "followers", "following"]
            X = np.array(
                [
                    [
                        input_data.get("post_count", 0),
                        input_data.get("avg_engagement_rate", 0),
                        input_data.get("followers", 0),
                        input_data.get("following", 0),
                    ]
                ]
            )

            # 스케일링
            scaler_path = self.models_path / "user_clustering_scaler.joblib"
            if scaler_path.exists():
                scaler = joblib.load(scaler_path)
                X_scaled = scaler.transform(X)
            else:
                X_scaled = X

            # 예측
            cluster = model.predict(X_scaled)[0]

            return {
                "predicted_cluster": int(cluster),
                "cluster_characteristics": f"클러스터 {cluster} 사용자",
            }

        except Exception as e:
            return {"error": f"사용자 클러스터 예측 실패: {str(e)}"}


async def main():
    """메인 실행 함수"""
    ai_pipeline = AIPipeline()

    # 데이터 로드
    data = await ai_pipeline.load_data()

    # 모델 학습
    await ai_pipeline.train_models(data)

    # 예측 테스트
    test_input = {
        "likes": 100,
        "comments": 20,
        "shares": 10,
        "hashtag_count": 5,
        "content_length": 200,
        "hour_of_day": 14,
    }

    prediction = await ai_pipeline.predict("engagement_prediction", test_input)
    logger.info(f"예측 결과: {prediction}")

    logger.info("AI 파이프라인 완료")


if __name__ == "__main__":
    asyncio.run(main())
