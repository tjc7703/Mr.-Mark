#!/usr/bin/env python3
"""
SNS 데이터 수집 파이프라인
Instagram, Facebook, Twitter, LinkedIn, TikTok 등 30개 플랫폼 데이터 수집
"""

import asyncio
import aiohttp
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
from dataclasses import dataclass
import os
from pathlib import Path

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SNSConfig:
    """SNS 플랫폼별 설정"""
    platform: str
    api_url: str
    api_key: str
    rate_limit: int  # 분당 요청 수
    endpoints: List[str]
    
class SNSDataCollector:
    """SNS 데이터 수집기"""
    
    def __init__(self):
        self.configs = self._load_sns_configs()
        self.session = None
        self.raw_data_path = Path("data/lake/raw/sns")
        self.raw_data_path.mkdir(parents=True, exist_ok=True)
        
    def _load_sns_configs(self) -> Dict[str, SNSConfig]:
        """SNS 플랫폼별 설정 로드"""
        return {
            'instagram': SNSConfig(
                platform='instagram',
                api_url='https://graph.instagram.com/v12.0',
                api_key=os.getenv('INSTAGRAM_API_KEY', ''),
                rate_limit=200,
                endpoints=['/me/media', '/me/stories']
            ),
            'facebook': SNSConfig(
                platform='facebook',
                api_url='https://graph.facebook.com/v12.0',
                api_key=os.getenv('FACEBOOK_API_KEY', ''),
                rate_limit=200,
                endpoints=['/me/posts', '/me/photos']
            ),
            'twitter': SNSConfig(
                platform='twitter',
                api_url='https://api.twitter.com/2',
                api_key=os.getenv('TWITTER_API_KEY', ''),
                rate_limit=300,
                endpoints=['/tweets', '/users/by/username']
            ),
            'linkedin': SNSConfig(
                platform='linkedin',
                api_url='https://api.linkedin.com/v2',
                api_key=os.getenv('LINKEDIN_API_KEY', ''),
                rate_limit=100,
                endpoints=['/posts', '/people']
            ),
            'tiktok': SNSConfig(
                platform='tiktok',
                api_url='https://open.tiktokapis.com/v2',
                api_key=os.getenv('TIKTOK_API_KEY', ''),
                rate_limit=100,
                endpoints=['/video/query', '/user/info']
            )
        }
    
    async def __aenter__(self):
        """비동기 컨텍스트 매니저 진입"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 종료"""
        if self.session:
            await self.session.close()
    
    async def collect_platform_data(self, platform: str, config: SNSConfig) -> Dict:
        """특정 플랫폼 데이터 수집"""
        try:
            logger.info(f"수집 시작: {platform}")
            
            collected_data = {
                'platform': platform,
                'timestamp': datetime.now().isoformat(),
                'posts': [],
                'comments': [],
                'likes': [],
                'shares': [],
                'hashtags': [],
                'users': []
            }
            
            # 각 엔드포인트에서 데이터 수집
            for endpoint in config.endpoints:
                data = await self._fetch_data(config, endpoint)
                if data:
                    collected_data['posts'].extend(data.get('posts', []))
                    collected_data['comments'].extend(data.get('comments', []))
                    collected_data['likes'].extend(data.get('likes', []))
                    collected_data['shares'].extend(data.get('shares', []))
                    collected_data['hashtags'].extend(data.get('hashtags', []))
                    collected_data['users'].extend(data.get('users', []))
            
            # 데이터 저장
            await self._save_data(platform, collected_data)
            
            logger.info(f"수집 완료: {platform} - {len(collected_data['posts'])}개 포스트")
            return collected_data
            
        except Exception as e:
            logger.error(f"수집 실패: {platform} - {str(e)}")
            return {}
    
    async def _fetch_data(self, config: SNSConfig, endpoint: str) -> Optional[Dict]:
        """API에서 데이터 가져오기"""
        try:
            headers = {
                'Authorization': f'Bearer {config.api_key}',
                'Content-Type': 'application/json'
            }
            
            url = f"{config.api_url}{endpoint}"
            params = {
                'limit': 100,
                'fields': 'id,message,created_time,likes,comments,shares'
            }
            
            async with self.session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_platform_data(config.platform, data)
                else:
                    logger.warning(f"API 요청 실패: {endpoint} - {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"데이터 가져오기 실패: {endpoint} - {str(e)}")
            return None
    
    def _parse_platform_data(self, platform: str, raw_data: Dict) -> Dict:
        """플랫폼별 데이터 파싱"""
        parsed_data = {
            'posts': [],
            'comments': [],
            'likes': [],
            'shares': [],
            'hashtags': [],
            'users': []
        }
        
        if platform == 'instagram':
            parsed_data = self._parse_instagram_data(raw_data)
        elif platform == 'facebook':
            parsed_data = self._parse_facebook_data(raw_data)
        elif platform == 'twitter':
            parsed_data = self._parse_twitter_data(raw_data)
        elif platform == 'linkedin':
            parsed_data = self._parse_linkedin_data(raw_data)
        elif platform == 'tiktok':
            parsed_data = self._parse_tiktok_data(raw_data)
        
        return parsed_data
    
    def _parse_instagram_data(self, data: Dict) -> Dict:
        """Instagram 데이터 파싱"""
        parsed = {'posts': [], 'comments': [], 'likes': [], 'shares': [], 'hashtags': [], 'users': []}
        
        for item in data.get('data', []):
            post = {
                'id': item.get('id'),
                'caption': item.get('caption'),
                'media_type': item.get('media_type'),
                'media_url': item.get('media_url'),
                'permalink': item.get('permalink'),
                'timestamp': item.get('timestamp'),
                'like_count': item.get('like_count', 0),
                'comments_count': item.get('comments_count', 0)
            }
            parsed['posts'].append(post)
            
            # 해시태그 추출
            if item.get('caption'):
                hashtags = self._extract_hashtags(item['caption'])
                parsed['hashtags'].extend(hashtags)
        
        return parsed
    
    def _parse_facebook_data(self, data: Dict) -> Dict:
        """Facebook 데이터 파싱"""
        parsed = {'posts': [], 'comments': [], 'likes': [], 'shares': [], 'hashtags': [], 'users': []}
        
        for item in data.get('data', []):
            post = {
                'id': item.get('id'),
                'message': item.get('message'),
                'created_time': item.get('created_time'),
                'type': item.get('type'),
                'likes_count': item.get('likes', {}).get('summary', {}).get('total_count', 0),
                'comments_count': item.get('comments', {}).get('summary', {}).get('total_count', 0),
                'shares_count': item.get('shares', {}).get('count', 0)
            }
            parsed['posts'].append(post)
            
            # 해시태그 추출
            if item.get('message'):
                hashtags = self._extract_hashtags(item['message'])
                parsed['hashtags'].extend(hashtags)
        
        return parsed
    
    def _parse_twitter_data(self, data: Dict) -> Dict:
        """Twitter 데이터 파싱"""
        parsed = {'posts': [], 'comments': [], 'likes': [], 'shares': [], 'hashtags': [], 'users': []}
        
        for item in data.get('data', []):
            tweet = {
                'id': item.get('id'),
                'text': item.get('text'),
                'created_at': item.get('created_at'),
                'public_metrics': item.get('public_metrics', {}),
                'entities': item.get('entities', {})
            }
            parsed['posts'].append(tweet)
            
            # 해시태그 추출
            if item.get('text'):
                hashtags = self._extract_hashtags(item['text'])
                parsed['hashtags'].extend(hashtags)
        
        return parsed
    
    def _parse_linkedin_data(self, data: Dict) -> Dict:
        """LinkedIn 데이터 파싱"""
        parsed = {'posts': [], 'comments': [], 'likes': [], 'shares': [], 'hashtags': [], 'users': []}
        
        for item in data.get('elements', []):
            post = {
                'id': item.get('id'),
                'author': item.get('author'),
                'lifecycleState': item.get('lifecycleState'),
                'specificContent': item.get('specificContent', {}),
                'visibility': item.get('visibility', {}),
                'created': item.get('created', {}),
                'lastModified': item.get('lastModified', {})
            }
            parsed['posts'].append(post)
        
        return parsed
    
    def _parse_tiktok_data(self, data: Dict) -> Dict:
        """TikTok 데이터 파싱"""
        parsed = {'posts': [], 'comments': [], 'likes': [], 'shares': [], 'hashtags': [], 'users': []}
        
        for item in data.get('data', {}).get('videos', []):
            video = {
                'id': item.get('id'),
                'title': item.get('title'),
                'description': item.get('description'),
                'duration': item.get('duration'),
                'height': item.get('height'),
                'width': item.get('width'),
                'share_url': item.get('share_url'),
                'embed_url': item.get('embed_url'),
                'like_count': item.get('like_count', 0),
                'comment_count': item.get('comment_count', 0),
                'share_count': item.get('share_count', 0),
                'view_count': item.get('view_count', 0)
            }
            parsed['posts'].append(video)
            
            # 해시태그 추출
            if item.get('description'):
                hashtags = self._extract_hashtags(item['description'])
                parsed['hashtags'].extend(hashtags)
        
        return parsed
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """텍스트에서 해시태그 추출"""
        import re
        hashtags = re.findall(r'#\w+', text)
        return hashtags
    
    async def _save_data(self, platform: str, data: Dict):
        """수집된 데이터 저장"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{platform}_{timestamp}.json"
        filepath = self.raw_data_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"데이터 저장: {filepath}")
    
    async def collect_all_platforms(self) -> Dict[str, Dict]:
        """모든 플랫폼 데이터 수집"""
        all_data = {}
        
        async with self:
            tasks = []
            for platform, config in self.configs.items():
                task = self.collect_platform_data(platform, config)
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, (platform, config) in enumerate(self.configs.items()):
                if isinstance(results[i], Exception):
                    logger.error(f"플랫폼 수집 실패: {platform} - {results[i]}")
                    all_data[platform] = {}
                else:
                    all_data[platform] = results[i]
        
        return all_data

async def main():
    """메인 실행 함수"""
    collector = SNSDataCollector()
    all_data = await collector.collect_all_platforms()
    
    # 수집 결과 요약
    total_posts = sum(len(data.get('posts', [])) for data in all_data.values())
    total_hashtags = sum(len(data.get('hashtags', [])) for data in all_data.values())
    
    logger.info(f"수집 완료 - 총 포스트: {total_posts}, 총 해시태그: {total_hashtags}")
    
    return all_data

if __name__ == "__main__":
    asyncio.run(main()) 