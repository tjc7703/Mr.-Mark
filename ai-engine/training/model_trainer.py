#!/usr/bin/env python3
"""
AI 모델 학습 파이프라인
트렌드 예측, 감정 분석, 콘텐츠 추천, 캠페인 최적화 모델 학습
"""

import logging
import json
import pickle
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    mean_squared_error,
    r2_score,
)
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """AI 모델 학습기"""

    def __init__(self):
        self.models = {
            "trend_prediction": TrendPredictionModel(),
            "sentiment_analysis": SentimentAnalysisModel(),
            "content_recommendation": ContentRecommendationModel(),
            "campaign_optimization": CampaignOptimizationModel(),
        }
        self.models_path = Path("ai-engine/models")
        self.models_path.mkdir(parents=True, exist_ok=True)
        self.scalers = {}
        self.encoders = {}

    def train_model(
        self, model_name: str, training_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """모델 학습 및 검증"""
        try:
            logger.info(f"모델 학습 시작: {model_name}")

            if model_name not in self.models:
                raise ValueError(f"알 수 없는 모델: {model_name}")

            model = self.models[model_name]

            # 데이터 전처리
            X_train, X_test, y_train, y_test = self._prepare_data(
                model_name, training_data
            )

            # 모델 학습
            model.fit(X_train, y_train)

            # 모델 평가
            evaluation_results = self._evaluate_model(model, X_test, y_test, model_name)

            # 모델 저장
            model_path = self._save_model(model_name, model)

            results = {
                "model_name": model_name,
                "training_timestamp": datetime.now().isoformat(),
                "evaluation": evaluation_results,
                "model_path": str(model_path),
                "status": "success",
            }

            logger.info(
                f"모델 학습 완료: {model_name} - 정확도: {evaluation_results.get('accuracy', 0):.3f}"
            )

            return results

        except Exception as e:
            logger.error(f"모델 학습 실패: {model_name} - {str(e)}")
            return {
                "model_name": model_name,
                "training_timestamp": datetime.now().isoformat(),
                "error": str(e),
                "status": "failed",
            }

    def _prepare_data(
        self, model_name: str, data: Dict[str, Any]
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """데이터 전처리"""
        if model_name == "trend_prediction":
            return self._prepare_trend_data(data)
        elif model_name == "sentiment_analysis":
            return self._prepare_sentiment_data(data)
        elif model_name == "content_recommendation":
            return self._prepare_recommendation_data(data)
        elif model_name == "campaign_optimization":
            return self._prepare_campaign_data(data)
        else:
            raise ValueError(f"알 수 없는 모델: {model_name}")

    def _prepare_trend_data(
        self, data: Dict[str, Any]
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """트렌드 예측 데이터 준비"""
        # 샘플 데이터 생성 (실제로는 실제 데이터 사용)
        np.random.seed(42)
        n_samples = 1000

        # 특성 생성
        features = {
            "post_count": np.random.poisson(50, n_samples),
            "like_count": np.random.poisson(200, n_samples),
            "comment_count": np.random.poisson(20, n_samples),
            "share_count": np.random.poisson(10, n_samples),
            "hashtag_count": np.random.poisson(5, n_samples),
            "hour_of_day": np.random.randint(0, 24, n_samples),
            "day_of_week": np.random.randint(0, 7, n_samples),
        }

        X = pd.DataFrame(features)

        # 타겟 생성 (트렌드 점수)
        trend_score = (
            features["like_count"] * 0.3
            + features["comment_count"] * 0.2
            + features["share_count"] * 0.5
            + np.random.normal(0, 10, n_samples)
        )

        # 트렌드 레이블 (상승/하락/유지)
        y = np.where(
            trend_score > np.percentile(trend_score, 70),
            "rising",
            np.where(trend_score < np.percentile(trend_score, 30), "falling", "stable"),
        )

        # 데이터 분할
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def _prepare_sentiment_data(
        self, data: Dict[str, Any]
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """감정 분석 데이터 준비"""
        # 샘플 텍스트 데이터
        texts = [
            "정말 좋은 제품이에요! 완벽합니다.",
            "이 영화는 최고예요! 감동적이었습니다.",
            "오늘 날씨가 너무 나빠요. 짜증나요.",
            "이 음식은 그저 그랬어요. 특별하지 않아요.",
            "훌륭한 서비스입니다. 추천해요!",
            "최악의 경험이었어요. 다시는 안 갈 거예요.",
            "보통이에요. 특별한 점이 없어요.",
            "정말 만족스러워요! 행복합니다.",
            "실망스러워요. 기대에 못 미쳐요.",
            "완벽해요! 최고의 선택이었습니다.",
        ] * 100  # 1000개 샘플

        # 감정 레이블
        labels = [
            "positive",
            "positive",
            "negative",
            "neutral",
            "positive",
            "negative",
            "neutral",
            "positive",
            "negative",
            "positive",
        ] * 100

        # TF-IDF 벡터화
        vectorizer = TfidfVectorizer(max_features=1000, stop_words="english")
        X = vectorizer.fit_transform(texts)

        # 레이블 인코딩
        encoder = LabelEncoder()
        y = encoder.fit_transform(labels)

        # 인코더 저장
        self.encoders["sentiment"] = encoder

        return train_test_split(X, y, test_size=0.2, random_state=42)

    def _prepare_recommendation_data(
        self, data: Dict[str, Any]
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """콘텐츠 추천 데이터 준비"""
        # 샘플 사용자-아이템 상호작용 데이터
        np.random.seed(42)
        n_users = 500
        n_items = 100
        n_interactions = 2000

        # 사용자-아이템 매트릭스 생성
        user_ids = np.random.randint(0, n_users, n_interactions)
        item_ids = np.random.randint(0, n_items, n_interactions)
        ratings = np.random.randint(1, 6, n_interactions)

        # 특성 생성
        features = {
            "user_id": user_ids,
            "item_id": item_ids,
            "user_avg_rating": np.random.uniform(2, 5, n_users)[user_ids],
            "item_avg_rating": np.random.uniform(2, 5, n_items)[item_ids],
            "user_interaction_count": np.random.poisson(10, n_users)[user_ids],
            "item_popularity": np.random.poisson(20, n_items)[item_ids],
        }

        X = pd.DataFrame(features)
        y = ratings

        return train_test_split(X, y, test_size=0.2, random_state=42)

    def _prepare_campaign_data(
        self, data: Dict[str, Any]
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """캠페인 최적화 데이터 준비"""
        # 샘플 캠페인 데이터
        np.random.seed(42)
        n_campaigns = 1000

        features = {
            "budget": np.random.uniform(1000, 10000, n_campaigns),
            "duration_days": np.random.randint(1, 30, n_campaigns),
            "target_audience_size": np.random.randint(1000, 100000, n_campaigns),
            "platform_count": np.random.randint(1, 5, n_campaigns),
            "content_type_count": np.random.randint(1, 4, n_campaigns),
            "hashtag_count": np.random.randint(0, 10, n_campaigns),
            "hour_of_day": np.random.randint(0, 24, n_campaigns),
            "day_of_week": np.random.randint(0, 7, n_campaigns),
        }

        X = pd.DataFrame(features)

        # 성공률 계산 (예측 타겟)
        success_rate = (
            features["budget"] * 0.0001
            + features["duration_days"] * 0.02
            + features["target_audience_size"] * 0.00001
            + features["platform_count"] * 0.1
            + features["content_type_count"] * 0.05
            + np.random.normal(0, 0.1, n_campaigns)
        )

        # 성공/실패 레이블
        y = (success_rate > np.median(success_rate)).astype(int)

        return train_test_split(X, y, test_size=0.2, random_state=42)

    def _evaluate_model(
        self, model, X_test: np.ndarray, y_test: np.ndarray, model_name: str
    ) -> Dict[str, float]:
        """모델 성능 평가"""
        try:
            y_pred = model.predict(X_test)

            if model_name == "sentiment_analysis":
                # 분류 모델 평가
                return {
                    "accuracy": accuracy_score(y_test, y_pred),
                    "precision": precision_score(y_test, y_pred, average="weighted"),
                    "recall": recall_score(y_test, y_pred, average="weighted"),
                    "f1_score": f1_score(y_test, y_pred, average="weighted"),
                }
            elif model_name == "trend_prediction":
                # 분류 모델 평가
                return {
                    "accuracy": accuracy_score(y_test, y_pred),
                    "precision": precision_score(y_test, y_pred, average="weighted"),
                    "recall": recall_score(y_test, y_pred, average="weighted"),
                    "f1_score": f1_score(y_test, y_pred, average="weighted"),
                }
            elif model_name == "content_recommendation":
                # 회귀 모델 평가
                return {
                    "mse": mean_squared_error(y_test, y_pred),
                    "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
                    "r2_score": r2_score(y_test, y_pred),
                    "mae": np.mean(np.abs(y_test - y_pred)),
                }
            elif model_name == "campaign_optimization":
                # 분류 모델 평가
                return {
                    "accuracy": accuracy_score(y_test, y_pred),
                    "precision": precision_score(y_test, y_pred),
                    "recall": recall_score(y_test, y_pred),
                    "f1_score": f1_score(y_test, y_pred),
                }
            else:
                return {"error": "Unknown model type"}

        except Exception as e:
            logger.error(f"모델 평가 실패: {str(e)}")
            return {"error": str(e)}

    def _save_model(self, model_name: str, model) -> Path:
        """모델 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_filename = f"{model_name}_{timestamp}.joblib"
        model_path = self.models_path / model_filename

        # 모델 저장
        joblib.dump(model, model_path)

        # 메타데이터 저장
        metadata = {
            "model_name": model_name,
            "timestamp": timestamp,
            "model_type": type(model).__name__,
            "features": (
                getattr(model, "feature_names_in_", []).tolist()
                if hasattr(model, "feature_names_in_")
                else []
            ),
        }

        metadata_path = model_path.with_suffix(".json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        logger.info(f"모델 저장: {model_path}")
        return model_path

    def load_model(self, model_path: str):
        """모델 로드"""
        try:
            model = joblib.load(model_path)
            logger.info(f"모델 로드: {model_path}")
            return model
        except Exception as e:
            logger.error(f"모델 로드 실패: {model_path} - {str(e)}")
            return None

    def predict(self, model_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """모델 예측"""
        try:
            # 최신 모델 로드
            model_files = list(self.models_path.glob(f"{model_name}_*.joblib"))
            if not model_files:
                raise ValueError(f"모델 파일 없음: {model_name}")

            latest_model_path = max(model_files, key=lambda x: x.stat().st_mtime)
            model = self.load_model(str(latest_model_path))

            if model is None:
                raise ValueError(f"모델 로드 실패: {model_name}")

            # 입력 데이터 전처리
            processed_data = self._preprocess_input(model_name, input_data)

            # 예측
            prediction = model.predict(processed_data)
            probability = (
                model.predict_proba(processed_data)
                if hasattr(model, "predict_proba")
                else None
            )

            return {
                "model_name": model_name,
                "prediction": (
                    prediction.tolist() if hasattr(prediction, "tolist") else prediction
                ),
                "probability": (
                    probability.tolist() if probability is not None else None
                ),
                "confidence": self._calculate_confidence(prediction, probability),
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"예측 실패: {model_name} - {str(e)}")
            return {
                "model_name": model_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def _preprocess_input(
        self, model_name: str, input_data: Dict[str, Any]
    ) -> np.ndarray:
        """입력 데이터 전처리"""
        if model_name == "sentiment_analysis":
            # 텍스트 데이터 처리
            text = input_data.get("text", "")
            vectorizer = TfidfVectorizer(max_features=1000, stop_words="english")
            # 실제로는 저장된 vectorizer를 사용해야 함
            return vectorizer.fit_transform([text])

        elif model_name in [
            "trend_prediction",
            "content_recommendation",
            "campaign_optimization",
        ]:
            # 수치 데이터 처리
            features = []
            for key in input_data:
                if isinstance(input_data[key], (int, float)):
                    features.append(input_data[key])

            return np.array(features).reshape(1, -1)

        else:
            raise ValueError(f"알 수 없는 모델: {model_name}")

    def _calculate_confidence(self, prediction, probability) -> float:
        """예측 신뢰도 계산"""
        if probability is not None:
            return float(np.max(probability))
        else:
            return 0.5  # 기본값


class TrendPredictionModel:
    """트렌드 예측 모델"""

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def fit(self, X, y):
        return self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)


class SentimentAnalysisModel:
    """감정 분석 모델"""

    def __init__(self):
        self.model = LogisticRegression(random_state=42, max_iter=1000)

    def fit(self, X, y):
        return self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)


class ContentRecommendationModel:
    """콘텐츠 추천 모델"""

    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def fit(self, X, y):
        return self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)


class CampaignOptimizationModel:
    """캠페인 최적화 모델"""

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def fit(self, X, y):
        return self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)


def main():
    """테스트 함수"""
    trainer = ModelTrainer()

    # 샘플 데이터로 모델 학습 테스트
    sample_data = {"posts": [], "users": [], "campaigns": []}

    # 각 모델 학습
    for model_name in trainer.models.keys():
        result = trainer.train_model(model_name, sample_data)
        print(f"모델 학습 결과: {model_name}")
        print(f"상태: {result['status']}")
        if result["status"] == "success":
            print(f"평가: {result['evaluation']}")
        else:
            print(f"오류: {result['error']}")
        print("---")


if __name__ == "__main__":
    main()
