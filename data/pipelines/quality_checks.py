#!/usr/bin/env python3
"""
데이터 품질 검증 시스템
데이터 완성도, 정확도, 일관성, 최신성 검증
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pandas as pd
from pathlib import Path
import numpy as np
from dataclasses import dataclass
import asyncio

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class QualityRule:
    """품질 검증 규칙"""

    name: str
    threshold: float
    weight: float = 1.0
    description: str = ""


class DataQualityChecker:
    """데이터 품질 검증기"""

    def __init__(self):
        self.rules = self._load_quality_rules()
        self.reports_path = Path("data/reports/quality")
        self.reports_path.mkdir(parents=True, exist_ok=True)

    def _load_quality_rules(self) -> Dict[str, QualityRule]:
        """품질 검증 규칙 로드"""
        return {
            "completeness": QualityRule(
                name="completeness",
                threshold=0.95,
                weight=1.0,
                description="95% 이상 완성도",
            ),
            "accuracy": QualityRule(
                name="accuracy",
                threshold=0.90,
                weight=1.0,
                description="90% 이상 정확도",
            ),
            "consistency": QualityRule(
                name="consistency",
                threshold=0.85,
                weight=1.0,
                description="85% 이상 일관성",
            ),
            "timeliness": QualityRule(
                name="timeliness",
                threshold=300,  # 5분
                weight=1.0,
                description="5분 이내 최신성",
            ),
            "validity": QualityRule(
                name="validity",
                threshold=0.95,
                weight=1.0,
                description="95% 이상 유효성",
            ),
            "uniqueness": QualityRule(
                name="uniqueness",
                threshold=0.98,
                weight=1.0,
                description="98% 이상 고유성",
            ),
        }

    def validate_data(self, data: Dict, data_type: str) -> Dict[str, Any]:
        """데이터 품질 검증"""
        try:
            logger.info(f"품질 검증 시작: {data_type}")

            validation_results = {
                "data_type": data_type,
                "timestamp": datetime.now().isoformat(),
                "overall_score": 0.0,
                "metrics": {},
                "issues": [],
                "recommendations": [],
            }

            # 각 품질 지표 검증
            completeness_score = self._check_completeness(data)
            accuracy_score = self._check_accuracy(data)
            consistency_score = self._check_consistency(data)
            timeliness_score = self._check_timeliness(data)
            validity_score = self._check_validity(data)
            uniqueness_score = self._check_uniqueness(data)

            # 결과 저장
            validation_results["metrics"] = {
                "completeness": completeness_score,
                "accuracy": accuracy_score,
                "consistency": consistency_score,
                "timeliness": timeliness_score,
                "validity": validity_score,
                "uniqueness": uniqueness_score,
            }

            # 전체 점수 계산
            scores = [
                completeness_score,
                accuracy_score,
                consistency_score,
                timeliness_score,
                validity_score,
                uniqueness_score,
            ]

            validation_results["overall_score"] = np.mean(scores)

            # 이슈 및 권장사항 생성
            validation_results["issues"] = self._identify_issues(
                validation_results["metrics"]
            )
            validation_results["recommendations"] = self._generate_recommendations(
                validation_results["metrics"]
            )

            logger.info(
                f"품질 검증 완료: {data_type} - 점수: {validation_results['overall_score']:.2f}"
            )

            return validation_results

        except Exception as e:
            logger.error(f"품질 검증 실패: {data_type} - {str(e)}")
            return {
                "data_type": data_type,
                "timestamp": datetime.now().isoformat(),
                "overall_score": 0.0,
                "metrics": {},
                "issues": [f"검증 중 오류 발생: {str(e)}"],
                "recommendations": ["데이터 형식 확인 필요"],
            }

    def _check_completeness(self, data: Dict) -> float:
        """완성도 검증"""
        try:
            if not data:
                return 0.0

            total_fields = 0
            filled_fields = 0

            # 필수 필드 정의
            required_fields = ["id", "timestamp", "platform"]

            for item in data.get("posts", []):
                total_fields += len(required_fields)
                for field in required_fields:
                    if item.get(field) is not None and item.get(field) != "":
                        filled_fields += 1

            if total_fields == 0:
                return 0.0

            return filled_fields / total_fields

        except Exception as e:
            logger.error(f"완성도 검증 실패: {str(e)}")
            return 0.0

    def _check_accuracy(self, data: Dict) -> float:
        """정확도 검증"""
        try:
            if not data:
                return 0.0

            total_items = 0
            accurate_items = 0

            for item in data.get("posts", []):
                total_items += 1

                # 기본 정확도 검증
                is_accurate = True

                # ID 형식 검증
                if "id" in item and not isinstance(item["id"], (str, int)):
                    is_accurate = False

                # 타임스탬프 형식 검증
                if "timestamp" in item:
                    try:
                        datetime.fromisoformat(item["timestamp"].replace("Z", "+00:00"))
                    except:
                        is_accurate = False

                # 플랫폼 값 검증
                if "platform" in item and item["platform"] not in [
                    "instagram",
                    "facebook",
                    "twitter",
                    "linkedin",
                    "tiktok",
                ]:
                    is_accurate = False

                if is_accurate:
                    accurate_items += 1

            if total_items == 0:
                return 0.0

            return accurate_items / total_items

        except Exception as e:
            logger.error(f"정확도 검증 실패: {str(e)}")
            return 0.0

    def _check_consistency(self, data: Dict) -> float:
        """일관성 검증"""
        try:
            if not data:
                return 0.0

            consistency_checks = 0
            consistent_items = 0

            for item in data.get("posts", []):
                consistency_checks += 1

                # 일관성 검증
                is_consistent = True

                # 필드 타입 일관성
                if "like_count" in item and not isinstance(
                    item["like_count"], (int, float)
                ):
                    is_consistent = False

                if "comment_count" in item and not isinstance(
                    item["comment_count"], (int, float)
                ):
                    is_consistent = False

                # 값 범위 일관성
                if "like_count" in item and item["like_count"] < 0:
                    is_consistent = False

                if "comment_count" in item and item["comment_count"] < 0:
                    is_consistent = False

                if is_consistent:
                    consistent_items += 1

            if consistency_checks == 0:
                return 0.0

            return consistent_items / consistency_checks

        except Exception as e:
            logger.error(f"일관성 검증 실패: {str(e)}")
            return 0.0

    def _check_timeliness(self, data: Dict) -> float:
        """최신성 검증"""
        try:
            if not data:
                return 0.0

            current_time = datetime.now()
            total_items = 0
            timely_items = 0

            for item in data.get("posts", []):
                if "timestamp" in item:
                    total_items += 1

                    try:
                        item_time = datetime.fromisoformat(
                            item["timestamp"].replace("Z", "+00:00")
                        )
                        time_diff = abs((current_time - item_time).total_seconds())

                        # 5분 이내면 최신으로 간주
                        if time_diff <= 300:
                            timely_items += 1

                    except:
                        pass

            if total_items == 0:
                return 0.0

            return timely_items / total_items

        except Exception as e:
            logger.error(f"최신성 검증 실패: {str(e)}")
            return 0.0

    def _check_validity(self, data: Dict) -> float:
        """유효성 검증"""
        try:
            if not data:
                return 0.0

            total_items = 0
            valid_items = 0

            for item in data.get("posts", []):
                total_items += 1

                # 유효성 검증
                is_valid = True

                # 필수 필드 존재 확인
                if not item.get("id"):
                    is_valid = False

                # URL 형식 검증 (있는 경우)
                if "media_url" in item and item["media_url"]:
                    if not item["media_url"].startswith(("http://", "https://")):
                        is_valid = False

                if is_valid:
                    valid_items += 1

            if total_items == 0:
                return 0.0

            return valid_items / total_items

        except Exception as e:
            logger.error(f"유효성 검증 실패: {str(e)}")
            return 0.0

    def _check_uniqueness(self, data: Dict) -> float:
        """고유성 검증"""
        try:
            if not data:
                return 0.0

            ids = []
            for item in data.get("posts", []):
                if "id" in item:
                    ids.append(item["id"])

            if not ids:
                return 0.0

            unique_ids = set(ids)
            return len(unique_ids) / len(ids)

        except Exception as e:
            logger.error(f"고유성 검증 실패: {str(e)}")
            return 0.0

    def _identify_issues(self, metrics: Dict[str, float]) -> List[str]:
        """품질 이슈 식별"""
        issues = []

        for metric_name, score in metrics.items():
            rule = self.rules.get(metric_name)
            if rule and score < rule.threshold:
                issues.append(f"{metric_name}: {score:.2f} < {rule.threshold} (목표)")

        return issues

    def _generate_recommendations(self, metrics: Dict[str, float]) -> List[str]:
        """개선 권장사항 생성"""
        recommendations = []

        if metrics.get("completeness", 1.0) < 0.95:
            recommendations.append("완성도 개선: 필수 필드 누락 데이터 보완 필요")

        if metrics.get("accuracy", 1.0) < 0.90:
            recommendations.append("정확도 개선: 데이터 형식 및 값 검증 강화 필요")

        if metrics.get("consistency", 1.0) < 0.85:
            recommendations.append("일관성 개선: 데이터 타입 및 값 범위 표준화 필요")

        if metrics.get("timeliness", 1.0) < 0.8:
            recommendations.append("최신성 개선: 실시간 데이터 수집 주기 단축 필요")

        if metrics.get("validity", 1.0) < 0.95:
            recommendations.append("유효성 개선: 데이터 검증 로직 강화 필요")

        if metrics.get("uniqueness", 1.0) < 0.98:
            recommendations.append("고유성 개선: 중복 데이터 제거 로직 강화 필요")

        return recommendations

    def generate_report(self, validation_results: Dict[str, Any]) -> str:
        """품질 보고서 생성"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = (
                f"quality_report_{validation_results['data_type']}_{timestamp}.json"
            )
            filepath = self.reports_path / filename

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(validation_results, f, ensure_ascii=False, indent=2)

            logger.info(f"품질 보고서 생성: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"보고서 생성 실패: {str(e)}")
            return ""

    async def validate_all_data(self, data_files: List[str]) -> Dict[str, Dict]:
        """모든 데이터 파일 품질 검증"""
        all_results = {}

        for file_path in data_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                data_type = Path(file_path).stem
                validation_result = self.validate_data(data, data_type)

                # 보고서 생성
                report_path = self.generate_report(validation_result)
                validation_result["report_path"] = report_path

                all_results[data_type] = validation_result

            except Exception as e:
                logger.error(f"파일 검증 실패: {file_path} - {str(e)}")
                all_results[Path(file_path).stem] = {
                    "error": str(e),
                    "overall_score": 0.0,
                }

        return all_results


async def main():
    """메인 실행 함수"""
    checker = DataQualityChecker()

    # 샘플 데이터로 테스트
    sample_data = {
        "posts": [
            {
                "id": "123",
                "platform": "instagram",
                "timestamp": datetime.now().isoformat(),
                "like_count": 100,
                "comment_count": 10,
            }
        ]
    }

    result = checker.validate_data(sample_data, "sample")
    report_path = checker.generate_report(result)

    logger.info(f"품질 검증 완료 - 점수: {result['overall_score']:.2f}")
    logger.info(f"보고서 경로: {report_path}")

    return result


if __name__ == "__main__":
    asyncio.run(main())
