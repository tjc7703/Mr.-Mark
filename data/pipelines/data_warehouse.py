#!/usr/bin/env python3
"""
데이터 웨어하우스 파이프라인
Raw 데이터 → 정제 → 웨어하우스 → 마트 구조
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
import sqlite3
import os

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DataMart:
    """데이터 마트 정의"""

    name: str
    description: str
    source_tables: List[str]
    aggregation_rules: Dict[str, str]
    refresh_schedule: str = "daily"


class DataWarehouse:
    """데이터 웨어하우스 관리"""

    def __init__(self):
        self.base_path = Path("data")
        self.lake_path = self.base_path / "lake"
        self.warehouse_path = self.base_path / "warehouse"
        self.marts_path = self.base_path / "marts"

        # 경로 생성
        for path in [self.lake_path, self.warehouse_path, self.marts_path]:
            path.mkdir(parents=True, exist_ok=True)

        self.db_path = self.warehouse_path / "warehouse.db"
        self.marts = self._define_marts()

    def _define_marts(self) -> Dict[str, DataMart]:
        """데이터 마트 정의"""
        return {
            "marketing_performance": DataMart(
                name="marketing_performance",
                description="마케팅 성과 지표",
                source_tables=["posts", "engagement", "users"],
                aggregation_rules={
                    "total_posts": "COUNT(*)",
                    "total_engagement": "SUM(likes + comments + shares)",
                    "avg_engagement_rate": "AVG((likes + comments + shares) / followers)",
                    "top_hashtags": "GROUP_CONCAT(hashtag ORDER BY count DESC LIMIT 10)",
                },
            ),
            "trend_analysis": DataMart(
                name="trend_analysis",
                description="트렌드 분석",
                source_tables=["posts", "hashtags", "trends"],
                aggregation_rules={
                    "trending_hashtags": "GROUP_CONCAT(hashtag ORDER BY trend_score DESC LIMIT 20)",
                    "peak_hours": "GROUP_CONCAT(hour ORDER BY post_count DESC LIMIT 5)",
                    "content_performance": "AVG(engagement_rate)",
                },
            ),
            "user_behavior": DataMart(
                name="user_behavior",
                description="사용자 행동 분석",
                source_tables=["users", "engagement", "posts"],
                aggregation_rules={
                    "active_users": "COUNT(DISTINCT user_id)",
                    "avg_session_duration": "AVG(session_duration)",
                    "retention_rate": "COUNT(DISTINCT user_id) / COUNT(DISTINCT total_users)",
                },
            ),
            "content_optimization": DataMart(
                name="content_optimization",
                description="콘텐츠 최적화",
                source_tables=["posts", "engagement", "content_types"],
                aggregation_rules={
                    "best_content_types": "GROUP_CONCAT(content_type ORDER BY avg_engagement DESC)",
                    "optimal_posting_times": "GROUP_CONCAT(posting_hour ORDER BY engagement_rate DESC LIMIT 5)",
                    "content_recommendations": "GROUP_CONCAT(recommendation ORDER BY priority DESC)",
                },
            ),
        }

    def init_database(self):
        """데이터베이스 초기화"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 테이블 생성
            tables = {
                "posts": """
                    CREATE TABLE IF NOT EXISTS posts (
                        id TEXT PRIMARY KEY,
                        platform TEXT,
                        content TEXT,
                        media_type TEXT,
                        created_at TIMESTAMP,
                        likes INTEGER DEFAULT 0,
                        comments INTEGER DEFAULT 0,
                        shares INTEGER DEFAULT 0,
                        hashtags TEXT,
                        user_id TEXT,
                        engagement_rate REAL DEFAULT 0.0
                    )
                """,
                "users": """
                    CREATE TABLE IF NOT EXISTS users (
                        id TEXT PRIMARY KEY,
                        platform TEXT,
                        username TEXT,
                        followers INTEGER DEFAULT 0,
                        following INTEGER DEFAULT 0,
                        posts_count INTEGER DEFAULT 0,
                        engagement_rate REAL DEFAULT 0.0,
                        last_active TIMESTAMP
                    )
                """,
                "hashtags": """
                    CREATE TABLE IF NOT EXISTS hashtags (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        hashtag TEXT,
                        platform TEXT,
                        post_count INTEGER DEFAULT 0,
                        engagement_count INTEGER DEFAULT 0,
                        trend_score REAL DEFAULT 0.0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """,
                "engagement": """
                    CREATE TABLE IF NOT EXISTS engagement (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        post_id TEXT,
                        user_id TEXT,
                        engagement_type TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (post_id) REFERENCES posts (id)
                    )
                """,
                "trends": """
                    CREATE TABLE IF NOT EXISTS trends (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        keyword TEXT,
                        platform TEXT,
                        trend_score REAL DEFAULT 0.0,
                        volume INTEGER DEFAULT 0,
                        growth_rate REAL DEFAULT 0.0,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """,
            }

            for table_name, schema in tables.items():
                cursor.execute(schema)
                logger.info(f"테이블 생성: {table_name}")

            conn.commit()
            conn.close()
            logger.info("데이터베이스 초기화 완료")

        except Exception as e:
            logger.error(f"데이터베이스 초기화 실패: {str(e)}")

    async def process_raw_data(self, raw_data_path: Path):
        """Raw 데이터 처리 및 웨어하우스 적재"""
        try:
            logger.info("Raw 데이터 처리 시작")

            # SNS 데이터 처리
            sns_path = raw_data_path / "sns"
            if sns_path.exists():
                await self._process_sns_data(sns_path)

            # 웹 데이터 처리
            web_path = raw_data_path / "web"
            if web_path.exists():
                await self._process_web_data(web_path)

            # CSV 데이터 처리
            csv_path = raw_data_path / "csv"
            if csv_path.exists():
                await self._process_csv_data(csv_path)

            logger.info("Raw 데이터 처리 완료")

        except Exception as e:
            logger.error(f"Raw 데이터 처리 실패: {str(e)}")

    async def _process_sns_data(self, sns_path: Path):
        """SNS 데이터 처리"""
        try:
            for platform_file in sns_path.glob("*.json"):
                with open(platform_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                platform = data.get("platform", "unknown")
                posts = data.get("posts", [])

                # 데이터베이스에 저장
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                for post in posts:
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO posts 
                        (id, platform, content, media_type, created_at, likes, comments, shares, hashtags, user_id, engagement_rate)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            post.get("id"),
                            platform,
                            post.get("caption", ""),
                            post.get("media_type", ""),
                            post.get("timestamp", ""),
                            post.get("like_count", 0),
                            post.get("comments_count", 0),
                            post.get("shares", 0),
                            ",".join(post.get("hashtags", [])),
                            post.get("user_id", ""),
                            self._calculate_engagement_rate(post),
                        ),
                    )

                conn.commit()
                conn.close()
                logger.info(f"SNS 데이터 처리 완료: {platform} - {len(posts)}개 포스트")

        except Exception as e:
            logger.error(f"SNS 데이터 처리 실패: {str(e)}")

    async def _process_web_data(self, web_path: Path):
        """웹 데이터 처리"""
        try:
            for web_file in web_path.glob("*.json"):
                with open(web_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # 웹 데이터를 웨어하우스 형식으로 변환
                processed_data = self._transform_web_data(data)

                # 데이터베이스에 저장
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                for item in processed_data:
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO posts 
                        (id, platform, content, created_at, likes, comments, shares)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            item.get("id"),
                            "web",
                            item.get("content", ""),
                            item.get("timestamp", ""),
                            item.get("likes", 0),
                            item.get("comments", 0),
                            item.get("shares", 0),
                        ),
                    )

                conn.commit()
                conn.close()
                logger.info(f"웹 데이터 처리 완료: {web_file.name}")

        except Exception as e:
            logger.error(f"웹 데이터 처리 실패: {str(e)}")

    async def _process_csv_data(self, csv_path: Path):
        """CSV 데이터 처리"""
        try:
            for csv_file in csv_path.glob("*.csv"):
                df = pd.read_csv(csv_file)

                # CSV 데이터를 웨어하우스 형식으로 변환
                processed_data = self._transform_csv_data(df)

                # 데이터베이스에 저장
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                for item in processed_data:
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO posts 
                        (id, platform, content, created_at, likes, comments, shares)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            item.get("id"),
                            "csv",
                            item.get("content", ""),
                            item.get("timestamp", ""),
                            item.get("likes", 0),
                            item.get("comments", 0),
                            item.get("shares", 0),
                        ),
                    )

                conn.commit()
                conn.close()
                logger.info(f"CSV 데이터 처리 완료: {csv_file.name}")

        except Exception as e:
            logger.error(f"CSV 데이터 처리 실패: {str(e)}")

    def _transform_web_data(self, data: Dict) -> List[Dict]:
        """웹 데이터를 웨어하우스 형식으로 변환"""
        transformed = []

        for item in data.get("articles", []):
            transformed.append(
                {
                    "id": item.get("id", f"web_{len(transformed)}"),
                    "content": item.get("title", "") + " " + item.get("content", ""),
                    "timestamp": item.get("published_at", ""),
                    "likes": item.get("likes", 0),
                    "comments": item.get("comments", 0),
                    "shares": item.get("shares", 0),
                }
            )

        return transformed

    def _transform_csv_data(self, df: pd.DataFrame) -> List[Dict]:
        """CSV 데이터를 웨어하우스 형식으로 변환"""
        transformed = []

        for _, row in df.iterrows():
            transformed.append(
                {
                    "id": str(row.get("id", f"csv_{len(transformed)}")),
                    "content": str(row.get("content", "")),
                    "timestamp": str(row.get("timestamp", "")),
                    "likes": int(row.get("likes", 0)),
                    "comments": int(row.get("comments", 0)),
                    "shares": int(row.get("shares", 0)),
                }
            )

        return transformed

    def _calculate_engagement_rate(self, post: Dict) -> float:
        """참여율 계산"""
        try:
            likes = post.get("like_count", 0)
            comments = post.get("comments_count", 0)
            shares = post.get("shares", 0)
            followers = post.get("followers", 1000)  # 기본값

            if followers > 0:
                return (likes + comments + shares) / followers
            return 0.0
        except:
            return 0.0

    async def build_marts(self):
        """데이터 마트 구축"""
        try:
            logger.info("데이터 마트 구축 시작")

            for mart_name, mart_config in self.marts.items():
                await self._build_mart(mart_name, mart_config)

            logger.info("데이터 마트 구축 완료")

        except Exception as e:
            logger.error(f"데이터 마트 구축 실패: {str(e)}")

    async def _build_mart(self, mart_name: str, mart_config: DataMart):
        """개별 마트 구축"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 마트별 집계 쿼리 실행
            if mart_name == "marketing_performance":
                await self._build_marketing_performance_mart(cursor)
            elif mart_name == "trend_analysis":
                await self._build_trend_analysis_mart(cursor)
            elif mart_name == "user_behavior":
                await self._build_user_behavior_mart(cursor)
            elif mart_name == "content_optimization":
                await self._build_content_optimization_mart(cursor)

            conn.commit()
            conn.close()

            logger.info(f"마트 구축 완료: {mart_name}")

        except Exception as e:
            logger.error(f"마트 구축 실패: {mart_name} - {str(e)}")

    async def _build_marketing_performance_mart(self, cursor):
        """마케팅 성과 마트 구축"""
        # 마케팅 성과 집계
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS marketing_performance AS
            SELECT 
                platform,
                COUNT(*) as total_posts,
                SUM(likes + comments + shares) as total_engagement,
                AVG((likes + comments + shares) / 1000.0) as avg_engagement_rate,
                DATE(created_at) as date
            FROM posts 
            GROUP BY platform, DATE(created_at)
        """
        )

    async def _build_trend_analysis_mart(self, cursor):
        """트렌드 분석 마트 구축"""
        # 트렌드 분석 집계
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS trend_analysis AS
            SELECT 
                hashtag,
                platform,
                COUNT(*) as usage_count,
                AVG(engagement_rate) as avg_engagement,
                DATE(created_at) as date
            FROM (
                SELECT 
                    p.*,
                    h.hashtag,
                    h.trend_score
                FROM posts p
                JOIN hashtags h ON p.hashtags LIKE '%' || h.hashtag || '%'
            )
            GROUP BY hashtag, platform, DATE(created_at)
            ORDER BY usage_count DESC
        """
        )

    async def _build_user_behavior_mart(self, cursor):
        """사용자 행동 마트 구축"""
        # 사용자 행동 집계
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_behavior AS
            SELECT 
                user_id,
                platform,
                COUNT(*) as post_count,
                AVG(engagement_rate) as avg_engagement_rate,
                SUM(likes + comments + shares) as total_engagement,
                DATE(created_at) as date
            FROM posts 
            WHERE user_id IS NOT NULL
            GROUP BY user_id, platform, DATE(created_at)
        """
        )

    async def _build_content_optimization_mart(self, cursor):
        """콘텐츠 최적화 마트 구축"""
        # 콘텐츠 최적화 집계
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS content_optimization AS
            SELECT 
                media_type,
                platform,
                COUNT(*) as content_count,
                AVG(engagement_rate) as avg_engagement_rate,
                AVG(likes) as avg_likes,
                AVG(comments) as avg_comments,
                AVG(shares) as avg_shares,
                strftime('%H', created_at) as posting_hour
            FROM posts 
            WHERE media_type IS NOT NULL
            GROUP BY media_type, platform, strftime('%H', created_at)
            ORDER BY avg_engagement_rate DESC
        """
        )


async def main():
    """메인 실행 함수"""
    warehouse = DataWarehouse()

    # 데이터베이스 초기화
    warehouse.init_database()

    # Raw 데이터 처리
    raw_data_path = Path("data/lake/raw")
    await warehouse.process_raw_data(raw_data_path)

    # 데이터 마트 구축
    await warehouse.build_marts()

    logger.info("데이터 웨어하우스 파이프라인 완료")


if __name__ == "__main__":
    asyncio.run(main())
