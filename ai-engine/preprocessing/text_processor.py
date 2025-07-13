#!/usr/bin/env python3
"""
텍스트 전처리 모듈
토큰화, 정규화, 불용어 제거, 감정 분석 등
"""

import re
import logging
from typing import List, Dict, Any, Optional
import numpy as np
from datetime import datetime
import json
from pathlib import Path
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
import emoji
import unicodedata

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextProcessor:
    """텍스트 전처리기"""

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words("english"))

        # 한국어 불용어 추가
        korean_stop_words = {
            "이",
            "그",
            "저",
            "것",
            "수",
            "등",
            "때",
            "곳",
            "말",
            "일",
            "때문",
            "그것",
            "그런",
            "이런",
            "저런",
            "어떤",
            "무슨",
            "어느",
            "아무",
            "모든",
            "각",
            "여러",
            "다른",
            "같은",
            "비슷한",
            "새로운",
            "옛날",
            "현재",
            "미래",
            "과거",
            "지금",
            "이제",
            "그때",
            "저때",
        }
        self.stop_words.update(korean_stop_words)

        # 감정 분석을 위한 감정 사전
        self.sentiment_dict = self._load_sentiment_dict()

    def _load_sentiment_dict(self) -> Dict[str, float]:
        """감정 사전 로드"""
        return {
            # 긍정적 단어들
            "좋다": 1.0,
            "훌륭하다": 1.0,
            "멋지다": 1.0,
            "완벽하다": 1.0,
            "최고": 1.0,
            "최고다": 1.0,
            "사랑": 1.0,
            "사랑한다": 1.0,
            "감동": 1.0,
            "감동적": 1.0,
            "행복": 1.0,
            "행복하다": 1.0,
            "즐겁다": 1.0,
            "재미있다": 1.0,
            "유용하다": 1.0,
            "도움이": 1.0,
            # 부정적 단어들
            "나쁘다": -1.0,
            "최악": -1.0,
            "최악이다": -1.0,
            "싫다": -1.0,
            "짜증": -1.0,
            "짜증나다": -1.0,
            "화나다": -1.0,
            "분노": -1.0,
            "실망": -1.0,
            "실망하다": -1.0,
            "슬프다": -1.0,
            "우울하다": -1.0,
            "힘들다": -1.0,
            "어렵다": -1.0,
            "복잡하다": -1.0,
            "불편하다": -1.0,
            # 중립적 단어들
            "보통": 0.0,
            "일반적": 0.0,
            "평범하다": 0.0,
            "그저": 0.0,
            "그냥": 0.0,
            "그대로": 0.0,
            "동일하다": 0.0,
            "같다": 0.0,
        }

    def preprocess_text(self, text: str, options: Dict[str, bool] = None) -> str:
        """텍스트 전처리 메인 함수"""
        if not text:
            return ""

        if options is None:
            options = {
                "normalize": True,
                "remove_emoji": True,
                "remove_urls": True,
                "remove_hashtags": False,
                "remove_mentions": True,
                "remove_numbers": False,
                "lowercase": True,
                "remove_stopwords": True,
                "lemmatize": True,
            }

        try:
            # 기본 정규화
            if options.get("normalize", True):
                text = self._normalize_text(text)

            # 이모지 제거
            if options.get("remove_emoji", True):
                text = self._remove_emoji(text)

            # URL 제거
            if options.get("remove_urls", True):
                text = self._remove_urls(text)

            # 해시태그 제거 (선택적)
            if options.get("remove_hashtags", False):
                text = self._remove_hashtags(text)

            # 멘션 제거
            if options.get("remove_mentions", True):
                text = self._remove_mentions(text)

            # 숫자 제거 (선택적)
            if options.get("remove_numbers", False):
                text = self._remove_numbers(text)

            # 소문자 변환
            if options.get("lowercase", True):
                text = text.lower()

            # 토큰화
            tokens = self._tokenize(text)

            # 불용어 제거
            if options.get("remove_stopwords", True):
                tokens = self._remove_stopwords(tokens)

            # 표제어 추출
            if options.get("lemmatize", True):
                tokens = self._lemmatize_tokens(tokens)

            # 전처리된 텍스트 재조합
            processed_text = " ".join(tokens)

            return processed_text

        except Exception as e:
            logger.error(f"텍스트 전처리 실패: {str(e)}")
            return text

    def _normalize_text(self, text: str) -> str:
        """텍스트 정규화"""
        # 유니코드 정규화
        text = unicodedata.normalize("NFKC", text)

        # 공백 정규화
        text = re.sub(r"\s+", " ", text)

        # 특수문자 정규화
        text = re.sub(r"[^\w\s가-힣]", " ", text)

        return text.strip()

    def _remove_emoji(self, text: str) -> str:
        """이모지 제거"""
        return emoji.replace_emojis(text, replace="")

    def _remove_urls(self, text: str) -> str:
        """URL 제거"""
        url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        return re.sub(url_pattern, "", text)

    def _remove_hashtags(self, text: str) -> str:
        """해시태그 제거"""
        hashtag_pattern = r"#\w+"
        return re.sub(hashtag_pattern, "", text)

    def _remove_mentions(self, text: str) -> str:
        """멘션 제거"""
        mention_pattern = r"@\w+"
        return re.sub(mention_pattern, "", text)

    def _remove_numbers(self, text: str) -> str:
        """숫자 제거"""
        return re.sub(r"\d+", "", text)

    def _tokenize(self, text: str) -> List[str]:
        """토큰화"""
        try:
            return word_tokenize(text)
        except:
            # NLTK 토큰화 실패 시 간단한 공백 기반 토큰화
            return text.split()

    def _remove_stopwords(self, tokens: List[str]) -> List[str]:
        """불용어 제거"""
        return [token for token in tokens if token.lower() not in self.stop_words]

    def _lemmatize_tokens(self, tokens: List[str]) -> List[str]:
        """표제어 추출"""
        lemmatized = []
        for token in tokens:
            try:
                # 영어 단어는 NLTK lemmatizer 사용
                if re.match(r"^[a-zA-Z]+$", token):
                    lemmatized.append(self.lemmatizer.lemmatize(token))
                else:
                    # 한국어는 그대로 유지
                    lemmatized.append(token)
            except:
                lemmatized.append(token)
        return lemmatized

    def extract_hashtags(self, text: str) -> List[str]:
        """해시태그 추출"""
        hashtag_pattern = r"#(\w+)"
        hashtags = re.findall(hashtag_pattern, text)
        return hashtags

    def extract_mentions(self, text: str) -> List[str]:
        """멘션 추출"""
        mention_pattern = r"@(\w+)"
        mentions = re.findall(mention_pattern, text)
        return mentions

    def extract_urls(self, text: str) -> List[str]:
        """URL 추출"""
        url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        urls = re.findall(url_pattern, text)
        return urls

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """감정 분석"""
        try:
            # 텍스트 전처리 (감정 분석용)
            processed_text = self.preprocess_text(
                text,
                {
                    "normalize": True,
                    "remove_emoji": True,
                    "remove_urls": True,
                    "remove_hashtags": False,
                    "remove_mentions": True,
                    "remove_numbers": False,
                    "lowercase": True,
                    "remove_stopwords": False,  # 감정 분석에서는 불용어 유지
                    "lemmatize": True,
                },
            )

            tokens = processed_text.split()

            # 감정 점수 계산
            positive_score = 0
            negative_score = 0
            neutral_score = 0

            for token in tokens:
                sentiment_value = self.sentiment_dict.get(token, 0)
                if sentiment_value > 0:
                    positive_score += sentiment_value
                elif sentiment_value < 0:
                    negative_score += abs(sentiment_value)
                else:
                    neutral_score += 1

            # 정규화
            total_tokens = len(tokens)
            if total_tokens > 0:
                positive_score /= total_tokens
                negative_score /= total_tokens
                neutral_score /= total_tokens

            # 전체 감정 점수
            overall_sentiment = positive_score - negative_score

            # 감정 분류
            if overall_sentiment > 0.1:
                sentiment_label = "positive"
            elif overall_sentiment < -0.1:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"

            return {
                "overall_sentiment": overall_sentiment,
                "sentiment_label": sentiment_label,
                "positive_score": positive_score,
                "negative_score": negative_score,
                "neutral_score": neutral_score,
                "confidence": min(abs(overall_sentiment), 1.0),
            }

        except Exception as e:
            logger.error(f"감정 분석 실패: {str(e)}")
            return {
                "overall_sentiment": 0.0,
                "sentiment_label": "neutral",
                "positive_score": 0.0,
                "negative_score": 0.0,
                "neutral_score": 1.0,
                "confidence": 0.0,
            }

    def extract_keywords(self, text: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """키워드 추출"""
        try:
            # 텍스트 전처리
            processed_text = self.preprocess_text(
                text,
                {
                    "normalize": True,
                    "remove_emoji": True,
                    "remove_urls": True,
                    "remove_hashtags": False,
                    "remove_mentions": True,
                    "remove_numbers": False,
                    "lowercase": True,
                    "remove_stopwords": True,
                    "lemmatize": True,
                },
            )

            tokens = processed_text.split()

            # 단어 빈도 계산
            word_freq = {}
            for token in tokens:
                if len(token) > 1:  # 1글자 단어 제외
                    word_freq[token] = word_freq.get(token, 0) + 1

            # 빈도순 정렬
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

            # 상위 k개 키워드 반환
            keywords = []
            for word, freq in sorted_words[:top_k]:
                keywords.append(
                    {
                        "word": word,
                        "frequency": freq,
                        "weight": freq / len(tokens) if tokens else 0,
                    }
                )

            return keywords

        except Exception as e:
            logger.error(f"키워드 추출 실패: {str(e)}")
            return []

    def extract_topics(
        self, texts: List[str], num_topics: int = 5
    ) -> List[Dict[str, Any]]:
        """토픽 추출 (간단한 버전)"""
        try:
            all_keywords = {}

            # 모든 텍스트에서 키워드 추출
            for text in texts:
                keywords = self.extract_keywords(text, top_k=20)
                for keyword in keywords:
                    word = keyword["word"]
                    if word in all_keywords:
                        all_keywords[word]["frequency"] += keyword["frequency"]
                        all_keywords[word]["documents"] += 1
                    else:
                        all_keywords[word]["frequency"] = keyword["frequency"]
                        all_keywords[word]["documents"] = 1

            # TF-IDF 스타일 점수 계산
            total_docs = len(texts)
            for word, data in all_keywords.items():
                tf = data["frequency"]
                idf = np.log(total_docs / data["documents"])
                data["tfidf_score"] = tf * idf

            # TF-IDF 점수순 정렬
            sorted_topics = sorted(
                all_keywords.items(), key=lambda x: x[1]["tfidf_score"], reverse=True
            )

            # 상위 토픽 반환
            topics = []
            for word, data in sorted_topics[:num_topics]:
                topics.append(
                    {
                        "topic": word,
                        "frequency": data["frequency"],
                        "tfidf_score": data["tfidf_score"],
                        "document_count": data["documents"],
                    }
                )

            return topics

        except Exception as e:
            logger.error(f"토픽 추출 실패: {str(e)}")
            return []

    def batch_process(
        self, texts: List[str], options: Dict[str, bool] = None
    ) -> List[Dict[str, Any]]:
        """배치 텍스트 처리"""
        results = []

        for i, text in enumerate(texts):
            try:
                # 기본 전처리
                processed_text = self.preprocess_text(text, options)

                # 감정 분석
                sentiment = self.analyze_sentiment(text)

                # 키워드 추출
                keywords = self.extract_keywords(text)

                # 해시태그, 멘션, URL 추출
                hashtags = self.extract_hashtags(text)
                mentions = self.extract_mentions(text)
                urls = self.extract_urls(text)

                results.append(
                    {
                        "index": i,
                        "original_text": text,
                        "processed_text": processed_text,
                        "sentiment": sentiment,
                        "keywords": keywords,
                        "hashtags": hashtags,
                        "mentions": mentions,
                        "urls": urls,
                        "word_count": len(processed_text.split()),
                        "char_count": len(text),
                    }
                )

            except Exception as e:
                logger.error(f"배치 처리 실패 (인덱스 {i}): {str(e)}")
                results.append({"index": i, "original_text": text, "error": str(e)})

        return results


def main():
    """테스트 함수"""
    processor = TextProcessor()

    # 테스트 텍스트
    test_texts = [
        "오늘 정말 좋은 하루였어요! #행복 #좋은날 @친구와 함께",
        "이 제품은 정말 최고예요! 완벽한 품질입니다.",
        "오늘 날씨가 너무 나빠서 짜증나요... 😡",
        "이 영화는 그저 그랬어요. 특별한 점이 없었습니다.",
    ]

    # 배치 처리 테스트
    results = processor.batch_process(test_texts)

    for result in results:
        print(f"원본: {result['original_text']}")
        print(f"전처리: {result['processed_text']}")
        print(
            f"감정: {result['sentiment']['sentiment_label']} ({result['sentiment']['overall_sentiment']:.2f})"
        )
        print(f"키워드: {[kw['word'] for kw in result['keywords'][:5]]}")
        print(f"해시태그: {result['hashtags']}")
        print("---")


if __name__ == "__main__":
    main()
