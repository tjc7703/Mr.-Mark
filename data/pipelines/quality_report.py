#!/usr/bin/env python3
"""
데이터 품질 자동 체크 및 리포트 시스템
품질 지표 시각화, 문제점 감지, 개선 권장사항 생성
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from pathlib import Path
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass
import asyncio
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class QualityMetric:
    """품질 지표"""

    name: str
    value: float
    threshold: float
    status: str  # 'good', 'warning', 'critical'
    description: str


@dataclass
class QualityIssue:
    """품질 이슈"""

    severity: str  # 'low', 'medium', 'high', 'critical'
    category: str
    description: str
    affected_records: int
    recommendation: str


class QualityReporter:
    """데이터 품질 리포트 생성기"""

    def __init__(self):
        self.warehouse_path = Path("data/warehouse/warehouse.db")
        self.reports_path = Path("data/reports/quality")
        self.reports_path.mkdir(parents=True, exist_ok=True)

        # 품질 임계값 설정
        self.thresholds = {
            "completeness": 0.95,
            "accuracy": 0.90,
            "consistency": 0.85,
            "timeliness": 300,  # 5분
            "validity": 0.95,
            "uniqueness": 0.98,
        }

    async def generate_quality_report(self) -> Dict[str, Any]:
        """전체 품질 리포트 생성"""
        try:
            logger.info("품질 리포트 생성 시작")

            # 데이터베이스 연결
            conn = sqlite3.connect(self.warehouse_path)

            # 각 테이블별 품질 검사
            tables = ["posts", "users", "hashtags", "engagement", "trends"]
            quality_results = {}

            for table in tables:
                quality_results[table] = await self._analyze_table_quality(conn, table)

            # 전체 품질 점수 계산
            overall_score = self._calculate_overall_score(quality_results)

            # 이슈 및 권장사항 생성
            issues = await self._identify_quality_issues(conn, quality_results)
            recommendations = await self._generate_recommendations(issues)

            # 리포트 생성
            report = {
                "timestamp": datetime.now().isoformat(),
                "overall_score": overall_score,
                "table_quality": quality_results,
                "issues": issues,
                "recommendations": recommendations,
                "summary": self._generate_summary(overall_score, issues),
            }

            # 리포트 저장
            report_path = (
                self.reports_path
                / f"quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            # 시각화 생성
            await self._create_visualizations(report)

            conn.close()
            logger.info("품질 리포트 생성 완료")

            return report

        except Exception as e:
            logger.error(f"품질 리포트 생성 실패: {str(e)}")
            return {"error": str(e)}

    async def _analyze_table_quality(
        self, conn: sqlite3.Connection, table: str
    ) -> Dict[str, Any]:
        """테이블별 품질 분석"""
        try:
            # 테이블 존재 여부 확인
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'"
            )
            if not cursor.fetchone():
                return {"error": f"테이블이 존재하지 않습니다: {table}"}

            # 기본 통계
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            total_records = cursor.fetchone()[0]

            if total_records == 0:
                return {"error": f"테이블이 비어있습니다: {table}"}

            # 품질 지표 계산
            metrics = {}

            # 완성도 (NULL 값 비율)
            completeness = await self._calculate_completeness(conn, table)
            metrics["completeness"] = completeness

            # 정확도 (데이터 형식 검증)
            accuracy = await self._calculate_accuracy(conn, table)
            metrics["accuracy"] = accuracy

            # 일관성 (데이터 패턴 검증)
            consistency = await self._calculate_consistency(conn, table)
            metrics["consistency"] = consistency

            # 최신성 (마지막 업데이트 시간)
            timeliness = await self._calculate_timeliness(conn, table)
            metrics["timeliness"] = timeliness

            # 유효성 (도메인 값 검증)
            validity = await self._calculate_validity(conn, table)
            metrics["validity"] = validity

            # 고유성 (중복 데이터 비율)
            uniqueness = await self._calculate_uniqueness(conn, table)
            metrics["uniqueness"] = uniqueness

            # 전체 점수 계산
            overall_score = np.mean(list(metrics.values()))

            return {
                "total_records": total_records,
                "metrics": metrics,
                "overall_score": overall_score,
                "status": self._get_quality_status(overall_score),
            }

        except Exception as e:
            logger.error(f"테이블 품질 분석 실패: {table} - {str(e)}")
            return {"error": str(e)}

    async def _calculate_completeness(
        self, conn: sqlite3.Connection, table: str
    ) -> float:
        """완성도 계산"""
        try:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()

            total_fields = 0
            null_fields = 0

            for column in columns:
                column_name = column[1]
                cursor.execute(
                    f"SELECT COUNT(*) FROM {table} WHERE {column_name} IS NULL"
                )
                null_count = cursor.fetchone()[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                total_count = cursor.fetchone()[0]

                total_fields += total_count
                null_fields += null_count

            if total_fields == 0:
                return 0.0

            return 1.0 - (null_fields / total_fields)

        except Exception as e:
            logger.error(f"완성도 계산 실패: {table} - {str(e)}")
            return 0.0

    async def _calculate_accuracy(self, conn: sqlite3.Connection, table: str) -> float:
        """정확도 계산"""
        try:
            cursor = conn.cursor()

            # 테이블별 정확도 검증 규칙
            accuracy_rules = {
                "posts": [
                    "id IS NOT NULL AND id != ''",
                    "platform IN ('instagram', 'facebook', 'twitter', 'linkedin', 'tiktok')",
                    "created_at IS NOT NULL",
                ],
                "users": [
                    "id IS NOT NULL AND id != ''",
                    "platform IN ('instagram', 'facebook', 'twitter', 'linkedin', 'tiktok')",
                    "followers >= 0",
                ],
                "hashtags": [
                    "hashtag IS NOT NULL AND hashtag != ''",
                    "post_count >= 0",
                ],
            }

            if table not in accuracy_rules:
                return 1.0  # 기본값

            rules = accuracy_rules[table]
            total_records = 0
            valid_records = 0

            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            total_records = cursor.fetchone()[0]

            if total_records == 0:
                return 0.0

            # 각 규칙에 대해 검증
            for rule in rules:
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {rule}")
                valid_count = cursor.fetchone()[0]
                valid_records += valid_count

            # 평균 정확도
            return valid_records / (total_records * len(rules))

        except Exception as e:
            logger.error(f"정확도 계산 실패: {table} - {str(e)}")
            return 0.0

    async def _calculate_consistency(
        self, conn: sqlite3.Connection, table: str
    ) -> float:
        """일관성 계산"""
        try:
            cursor = conn.cursor()

            # 테이블별 일관성 검증
            consistency_checks = {
                "posts": [
                    "SELECT COUNT(*) FROM posts WHERE likes < 0 OR comments < 0 OR shares < 0",
                    "SELECT COUNT(*) FROM posts WHERE engagement_rate > 1.0",
                ],
                "users": [
                    "SELECT COUNT(*) FROM users WHERE followers < 0 OR following < 0"
                ],
            }

            if table not in consistency_checks:
                return 1.0  # 기본값

            checks = consistency_checks[table]
            total_records = 0
            consistent_records = 0

            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            total_records = cursor.fetchone()[0]

            if total_records == 0:
                return 0.0

            # 각 검증 규칙에 대해 확인
            for check in checks:
                cursor.execute(check)
                inconsistent_count = cursor.fetchone()[0]
                consistent_records += total_records - inconsistent_count

            return consistent_records / (total_records * len(checks))

        except Exception as e:
            logger.error(f"일관성 계산 실패: {table} - {str(e)}")
            return 0.0

    async def _calculate_timeliness(
        self, conn: sqlite3.Connection, table: str
    ) -> float:
        """최신성 계산"""
        try:
            cursor = conn.cursor()

            # timestamp 컬럼이 있는지 확인
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cursor.fetchall()]

            if "created_at" in columns:
                cursor.execute(f"SELECT MAX(created_at) FROM {table}")
                latest_time = cursor.fetchone()[0]

                if latest_time:
                    latest_dt = datetime.fromisoformat(
                        latest_time.replace("Z", "+00:00")
                    )
                    time_diff = (
                        datetime.now().replace(tzinfo=latest_dt.tzinfo) - latest_dt
                    )

                    # 5분 이내면 1.0, 그 외에는 비례하여 감소
                    if time_diff.total_seconds() <= 300:  # 5분
                        return 1.0
                    else:
                        return max(
                            0.0, 1.0 - (time_diff.total_seconds() - 300) / 3600
                        )  # 1시간당 0.1 감소

            return 0.5  # 기본값

        except Exception as e:
            logger.error(f"최신성 계산 실패: {table} - {str(e)}")
            return 0.0

    async def _calculate_validity(self, conn: sqlite3.Connection, table: str) -> float:
        """유효성 계산"""
        try:
            cursor = conn.cursor()

            # 테이블별 유효성 검증
            validity_rules = {
                "posts": [
                    "LENGTH(content) <= 10000",  # 콘텐츠 길이 제한
                    "likes >= 0 AND likes <= 1000000",  # 좋아요 수 범위
                    "comments >= 0 AND comments <= 100000",  # 댓글 수 범위
                ],
                "users": [
                    "followers >= 0 AND followers <= 10000000",  # 팔로워 수 범위
                    "following >= 0 AND following <= 10000",  # 팔로잉 수 범위
                ],
            }

            if table not in validity_rules:
                return 1.0  # 기본값

            rules = validity_rules[table]
            total_records = 0
            valid_records = 0

            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            total_records = cursor.fetchone()[0]

            if total_records == 0:
                return 0.0

            # 각 규칙에 대해 검증
            for rule in rules:
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {rule}")
                valid_count = cursor.fetchone()[0]
                valid_records += valid_count

            return valid_records / (total_records * len(rules))

        except Exception as e:
            logger.error(f"유효성 계산 실패: {table} - {str(e)}")
            return 0.0

    async def _calculate_uniqueness(
        self, conn: sqlite3.Connection, table: str
    ) -> float:
        """고유성 계산"""
        try:
            cursor = conn.cursor()

            # 테이블별 고유성 검증
            uniqueness_checks = {"posts": "id", "users": "id", "hashtags": "hashtag"}

            if table not in uniqueness_checks:
                return 1.0  # 기본값

            unique_column = uniqueness_checks[table]

            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            total_records = cursor.fetchone()[0]

            cursor.execute(f"SELECT COUNT(DISTINCT {unique_column}) FROM {table}")
            unique_records = cursor.fetchone()[0]

            if total_records == 0:
                return 0.0

            return unique_records / total_records

        except Exception as e:
            logger.error(f"고유성 계산 실패: {table} - {str(e)}")
            return 0.0

    def _get_quality_status(self, score: float) -> str:
        """품질 상태 판정"""
        if score >= 0.9:
            return "excellent"
        elif score >= 0.8:
            return "good"
        elif score >= 0.7:
            return "warning"
        else:
            return "critical"

    def _calculate_overall_score(self, quality_results: Dict[str, Any]) -> float:
        """전체 품질 점수 계산"""
        scores = []

        for table, result in quality_results.items():
            if isinstance(result, dict) and "overall_score" in result:
                scores.append(result["overall_score"])

        return np.mean(scores) if scores else 0.0

    async def _identify_quality_issues(
        self, conn: sqlite3.Connection, quality_results: Dict[str, Any]
    ) -> List[QualityIssue]:
        """품질 이슈 식별"""
        issues = []

        for table, result in quality_results.items():
            if isinstance(result, dict) and "metrics" in result:
                metrics = result["metrics"]

                # 각 지표별 이슈 확인
                for metric_name, score in metrics.items():
                    threshold = self.thresholds.get(metric_name, 0.8)

                    if score < threshold:
                        severity = (
                            "critical"
                            if score < threshold * 0.5
                            else "high" if score < threshold * 0.8 else "medium"
                        )

                        issue = QualityIssue(
                            severity=severity,
                            category=f"{table}_{metric_name}",
                            description=f"{table} 테이블의 {metric_name} 지표가 임계값({threshold}) 미달: {score:.3f}",
                            affected_records=result.get("total_records", 0),
                            recommendation=self._get_recommendation(metric_name, table),
                        )
                        issues.append(issue)

        return issues

    def _get_recommendation(self, metric_name: str, table: str) -> str:
        """개선 권장사항 생성"""
        recommendations = {
            "completeness": f"{table} 테이블의 NULL 값 처리가 필요합니다. 데이터 수집 과정에서 필수 필드 검증을 강화하세요.",
            "accuracy": f"{table} 테이블의 데이터 형식 검증이 필요합니다. 데이터 변환 과정에서 타입 체크를 추가하세요.",
            "consistency": f"{table} 테이블의 데이터 일관성 검증이 필요합니다. 비즈니스 규칙에 맞는 데이터 검증을 추가하세요.",
            "timeliness": f"{table} 테이블의 데이터가 오래되었습니다. 데이터 수집 주기를 단축하거나 실시간 업데이트를 고려하세요.",
            "validity": f"{table} 테이블의 데이터 유효성 검증이 필요합니다. 도메인 규칙에 맞는 값 범위 검증을 추가하세요.",
            "uniqueness": f"{table} 테이블에 중복 데이터가 있습니다. 데이터 정제 과정에서 중복 제거 로직을 추가하세요.",
        }

        return recommendations.get(
            metric_name, f"{table} 테이블의 데이터 품질 개선이 필요합니다."
        )

    async def _generate_recommendations(self, issues: List[QualityIssue]) -> List[str]:
        """전체 권장사항 생성"""
        recommendations = []

        # 심각도별 정렬
        critical_issues = [issue for issue in issues if issue.severity == "critical"]
        high_issues = [issue for issue in issues if issue.severity == "high"]

        if critical_issues:
            recommendations.append(
                "🚨 긴급 조치 필요: 데이터 품질이 심각한 수준입니다. 즉시 데이터 검증 및 정제 작업을 수행하세요."
            )

        if high_issues:
            recommendations.append(
                "⚠️ 주의 필요: 데이터 품질 개선이 필요합니다. 데이터 파이프라인 검토를 권장합니다."
            )

        # 카테고리별 권장사항
        categories = {}
        for issue in issues:
            if issue.category not in categories:
                categories[issue.category] = []
            categories[issue.category].append(issue.recommendation)

        for category, recs in categories.items():
            recommendations.append(f"📊 {category}: {recs[0]}")

        if not recommendations:
            recommendations.append(
                "✅ 데이터 품질이 양호합니다. 현재 상태를 유지하세요."
            )

        return recommendations

    def _generate_summary(
        self, overall_score: float, issues: List[QualityIssue]
    ) -> str:
        """요약 생성"""
        critical_count = len([i for i in issues if i.severity == "critical"])
        high_count = len([i for i in issues if i.severity == "high"])

        if overall_score >= 0.9:
            status = "우수"
        elif overall_score >= 0.8:
            status = "양호"
        elif overall_score >= 0.7:
            status = "주의"
        else:
            status = "심각"

        return f"전체 품질 점수: {overall_score:.3f} ({status}). 심각한 이슈 {critical_count}개, 주의 이슈 {high_count}개 발견."

    async def _create_visualizations(self, report: Dict[str, Any]):
        """품질 리포트 시각화 생성"""
        try:
            # 1. 전체 품질 점수 대시보드
            fig = make_subplots(
                rows=2,
                cols=2,
                subplot_titles=(
                    "전체 품질 점수",
                    "테이블별 품질",
                    "이슈 심각도 분포",
                    "품질 지표별 점수",
                ),
                specs=[
                    [{"type": "indicator"}, {"type": "bar"}],
                    [{"type": "pie"}, {"type": "radar"}],
                ],
            )

            # 전체 품질 점수 게이지
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=report["overall_score"],
                    domain={"x": [0, 1], "y": [0, 1]},
                    title={"text": "전체 품질 점수"},
                    gauge={
                        "axis": {"range": [None, 1]},
                        "bar": {"color": "darkblue"},
                        "steps": [
                            {"range": [0, 0.7], "color": "lightgray"},
                            {"range": [0.7, 0.9], "color": "yellow"},
                            {"range": [0.9, 1], "color": "green"},
                        ],
                        "threshold": {
                            "line": {"color": "red", "width": 4},
                            "thickness": 0.75,
                            "value": 0.9,
                        },
                    },
                ),
                row=1,
                col=1,
            )

            # 테이블별 품질 바 차트
            tables = list(report["table_quality"].keys())
            scores = [
                report["table_quality"][table].get("overall_score", 0)
                for table in tables
            ]

            fig.add_trace(go.Bar(x=tables, y=scores, name="품질 점수"), row=1, col=2)

            # 이슈 심각도 파이 차트
            severity_counts = {}
            for issue in report["issues"]:
                severity_counts[issue.severity] = (
                    severity_counts.get(issue.severity, 0) + 1
                )

            fig.add_trace(
                go.Pie(
                    labels=list(severity_counts.keys()),
                    values=list(severity_counts.values()),
                ),
                row=2,
                col=1,
            )

            # 품질 지표별 점수 레이더 차트
            if "posts" in report["table_quality"]:
                metrics = list(report["table_quality"]["posts"]["metrics"].keys())
                values = list(report["table_quality"]["posts"]["metrics"].values())

                fig.add_trace(
                    go.Scatterpolar(
                        r=values, theta=metrics, fill="toself", name="posts"
                    ),
                    row=2,
                    col=2,
                )

            fig.update_layout(height=800, title_text="데이터 품질 리포트")

            # HTML 파일로 저장
            viz_path = (
                self.reports_path
                / f"quality_visualization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            )
            fig.write_html(str(viz_path))

            logger.info(f"시각화 생성 완료: {viz_path}")

        except Exception as e:
            logger.error(f"시각화 생성 실패: {str(e)}")


async def main():
    """메인 실행 함수"""
    reporter = QualityReporter()

    # 품질 리포트 생성
    report = await reporter.generate_quality_report()

    # 결과 출력
    print(f"전체 품질 점수: {report.get('overall_score', 0):.3f}")
    print(f"발견된 이슈: {len(report.get('issues', []))}개")
    print(f"권장사항: {len(report.get('recommendations', []))}개")

    logger.info("품질 리포트 시스템 완료")


if __name__ == "__main__":
    asyncio.run(main())
