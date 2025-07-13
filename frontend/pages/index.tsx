"use client";

import React, { useState, useEffect } from 'react';
import { ExternalLinkIcon, CheckCircleIcon, XCircleIcon, TrendingUpIcon, LightBulbIcon, CogIcon } from '@heroicons/react/outline';

interface NewsItem {
  id: number;
  title: string;
  summary: string;
  source: string;
  url: string;
  published_at: string;
  category: string;
}

interface TrendItem {
  keyword: string;
  volume: number;
  growth: string;
  url: string;
}

interface ChecklistItem {
  task: string;
  completed: boolean;
}

interface AISuggestion {
  type: string;
  message: string;
  priority: string;
}

export default function Home() {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [trends, setTrends] = useState<TrendItem[]>([]);
  const [goals, setGoals] = useState<any>({});
  const [aiFeedback, setAiFeedback] = useState<AISuggestion[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [newsRes, trendsRes, goalsRes, feedbackRes] = await Promise.all([
          fetch('http://localhost:8000/feed/today'),
          fetch('http://localhost:8000/trend'),
          fetch('http://localhost:8000/goal'),
          fetch('http://localhost:8000/ai/feedback')
        ]);

        const newsData = await newsRes.json();
        const trendsData = await trendsRes.json();
        const goalsData = await goalsRes.json();
        const feedbackData = await feedbackRes.json();

        setNews(newsData.news || []);
        setTrends(trendsData.trends || []);
        setGoals(goalsData);
        setAiFeedback(feedbackData.suggestions || []);
      } catch (error) {
        console.error('데이터 로딩 중 오류:', error);
        // 오류 시 더미 데이터 사용
        setNews([
          {
            id: 1,
            title: "2024년 디지털 마케팅 트렌드: AI와 개인화가 주도",
            summary: "AI 기반 개인화 마케팅이 2024년의 핵심 트렌드로 부상하고 있습니다.",
            source: "마케팅 인사이트",
            url: "https://www.marketinginsight.co.kr/2024-digital-marketing-trends",
            published_at: "2024-01-15T10:30:00Z",
            category: "트렌드"
          }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-50';
      case 'medium': return 'text-yellow-600 bg-yellow-50';
      case 'low': return 'text-green-600 bg-green-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">데이터를 불러오는 중...</p>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900">Mr. Mark 마케팅 마스터리 대시보드</h1>
          <a
            href="/dashboard"
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
          >
            <CogIcon className="h-5 w-5 mr-2" />
            파이프라인 대시보드
          </a>
        </div>
        
        {/* 실시간 뉴스 피드 */}
        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 flex items-center">
            <TrendingUpIcon className="h-6 w-6 mr-2 text-blue-600" />
            오늘의 마케팅 뉴스
          </h2>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {news.map((item) => (
              <div key={item.id} className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200">
                <div className="p-6">
                  <div className="flex items-center justify-between mb-3">
                    <span className="inline-block px-2 py-1 text-xs font-medium text-blue-600 bg-blue-100 rounded-full">
                      {item.category}
                    </span>
                    <span className="text-xs text-gray-500">{item.source}</span>
                  </div>
                  <h3 className="text-lg font-semibold mb-2 text-gray-900 line-clamp-2">
                    {item.title}
                  </h3>
                  <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                    {item.summary}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">
                      {formatDate(item.published_at)}
                    </span>
                    <a
                      href={item.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors duration-200"
                    >
                      자세히 보기
                      <ExternalLinkIcon className="h-4 w-4 ml-1" />
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* 실시간 트렌드 */}
        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800">실시간 마케팅 트렌드</h2>
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {trends.map((trend, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors duration-200">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-medium text-gray-900">{trend.keyword}</h3>
                    <span className="text-green-600 text-sm font-medium">{trend.growth}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">검색량: {trend.volume.toLocaleString()}</span>
                    <a
                      href={trend.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 text-sm flex items-center"
                    >
                      트렌드 보기
                      <ExternalLinkIcon className="h-3 w-3 ml-1" />
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 목표 및 체크리스트 */}
        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800">오늘의 목표 & 체크리스트</h2>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold mb-4 text-gray-900">목표</h3>
              <div className="space-y-3">
                <div className="flex items-center p-3 bg-blue-50 rounded-lg">
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">일일 목표</p>
                    <p className="text-sm text-gray-600">{goals.daily_goal}</p>
                  </div>
                </div>
                <div className="flex items-center p-3 bg-green-50 rounded-lg">
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">주간 목표</p>
                    <p className="text-sm text-gray-600">{goals.weekly_goal}</p>
                  </div>
                </div>
                <div className="flex items-center p-3 bg-purple-50 rounded-lg">
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">월간 목표</p>
                    <p className="text-sm text-gray-600">{goals.monthly_goal}</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold mb-4 text-gray-900">체크리스트</h3>
              <div className="space-y-3">
                {goals.checklist?.map((item: ChecklistItem, index: number) => (
                  <div key={index} className="flex items-center p-3 border border-gray-200 rounded-lg">
                    {item.completed ? (
                      <CheckCircleIcon className="h-5 w-5 text-green-600 mr-3" />
                    ) : (
                      <XCircleIcon className="h-5 w-5 text-gray-400 mr-3" />
                    )}
                    <span className={`flex-1 ${item.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                      {item.task}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* AI 피드백 */}
        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 flex items-center">
            <LightBulbIcon className="h-6 w-6 mr-2 text-yellow-600" />
            AI 마케팅 피드백
          </h2>
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {aiFeedback.map((suggestion, index) => (
                <div key={index} className={`p-4 rounded-lg border-l-4 ${getPriorityColor(suggestion.priority)}`}>
                  <div className="flex items-start">
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900 mb-1">{suggestion.type}</h3>
                      <p className="text-sm text-gray-700">{suggestion.message}</p>
                    </div>
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      suggestion.priority === 'high' ? 'bg-red-100 text-red-800' :
                      suggestion.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {suggestion.priority === 'high' ? '높음' : 
                       suggestion.priority === 'medium' ? '보통' : '낮음'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>
    </main>
  );
} 