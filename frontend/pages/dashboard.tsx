"use client";

import React, { useState, useEffect } from 'react';
import { 
  ChartBarIcon, 
  CogIcon, 
  ExclamationCircleIcon, 
  CheckCircleIcon,
  TrendingUpIcon,
  UserGroupIcon,
  ClockIcon,
  DatabaseIcon
} from '@heroicons/react/outline';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface PipelineStatus {
  name: string;
  status: 'running' | 'completed' | 'failed' | 'idle';
  lastRun: string;
  duration: number;
  recordsProcessed: number;
}

interface QualityMetric {
  name: string;
  value: number;
  threshold: number;
  status: 'good' | 'warning' | 'critical';
}

interface AIModelPerformance {
  name: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1Score: number;
  lastTrained: string;
}

interface DataQualityIssue {
  severity: 'low' | 'medium' | 'high' | 'critical';
  category: string;
  description: string;
  affectedRecords: number;
  recommendation: string;
}

export default function Dashboard() {
  const [pipelineStatus, setPipelineStatus] = useState<PipelineStatus[]>([]);
  const [qualityMetrics, setQualityMetrics] = useState<QualityMetric[]>([]);
  const [aiModelPerformance, setAiModelPerformance] = useState<AIModelPerformance[]>([]);
  const [qualityIssues, setQualityIssues] = useState<DataQualityIssue[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // 파이프라인 상태 데이터
        const pipelineRes = await fetch('http://localhost:8000/pipeline/status');
        const pipelineData = await pipelineRes.json();
        setPipelineStatus(pipelineData.pipelines || []);

        // 품질 메트릭 데이터
        const qualityRes = await fetch('http://localhost:8000/quality/metrics');
        const qualityData = await qualityRes.json();
        setQualityMetrics(qualityData.metrics || []);

        // AI 모델 성능 데이터
        const aiRes = await fetch('http://localhost:8000/ai/performance');
        const aiData = await aiRes.json();
        setAiModelPerformance(aiData.models || []);

        // 품질 이슈 데이터
        const issuesRes = await fetch('http://localhost:8000/quality/issues');
        const issuesData = await issuesRes.json();
        setQualityIssues(issuesData.issues || []);

      } catch (error) {
        console.error('대시보드 데이터 로딩 실패:', error);
        // 더미 데이터 사용
        setPipelineStatus([
          {
            name: 'SNS 데이터 수집',
            status: 'completed',
            lastRun: '2024-01-15T10:30:00Z',
            duration: 120,
            recordsProcessed: 1500
          },
          {
            name: '데이터 정제',
            status: 'running',
            lastRun: '2024-01-15T10:35:00Z',
            duration: 45,
            recordsProcessed: 1200
          },
          {
            name: 'AI 모델 학습',
            status: 'completed',
            lastRun: '2024-01-15T09:00:00Z',
            duration: 1800,
            recordsProcessed: 800
          }
        ]);

        setQualityMetrics([
          { name: '완성도', value: 0.95, threshold: 0.9, status: 'good' },
          { name: '정확도', value: 0.88, threshold: 0.9, status: 'warning' },
          { name: '일관성', value: 0.92, threshold: 0.85, status: 'good' },
          { name: '최신성', value: 0.78, threshold: 0.8, status: 'warning' }
        ]);

        setAiModelPerformance([
          {
            name: '참여율 예측',
            accuracy: 0.85,
            precision: 0.82,
            recall: 0.88,
            f1Score: 0.85,
            lastTrained: '2024-01-15T09:00:00Z'
          },
          {
            name: '트렌드 예측',
            accuracy: 0.78,
            precision: 0.75,
            recall: 0.80,
            f1Score: 0.77,
            lastTrained: '2024-01-15T08:30:00Z'
          }
        ]);

        setQualityIssues([
          {
            severity: 'medium',
            category: 'posts_accuracy',
            description: 'posts 테이블의 정확도가 임계값 미달',
            affectedRecords: 150,
            recommendation: '데이터 형식 검증 강화 필요'
          }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600 bg-green-100';
      case 'running': return 'text-blue-600 bg-blue-100';
      case 'failed': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'text-red-600 bg-red-100';
      case 'high': return 'text-orange-600 bg-orange-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      default: return 'text-green-600 bg-green-100';
    }
  };

  const formatDuration = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds}s`;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('ko-KR');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">대시보드 데이터를 불러오는 중...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">데이터/AI 파이프라인 대시보드</h1>
          <p className="text-gray-600">실시간 파이프라인 상태, 데이터 품질, AI 모델 성능 모니터링</p>
        </div>

        {/* 탭 네비게이션 */}
        <div className="mb-6">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', name: '개요', icon: ChartBarIcon },
              { id: 'pipeline', name: '파이프라인', icon: CogIcon },
              { id: 'quality', name: '품질', icon: CheckCircleIcon },
              { id: 'ai', name: 'AI 모델', icon: TrendingUpIcon }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium ${
                  activeTab === tab.id
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <tab.icon className="h-5 w-5" />
                <span>{tab.name}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* 개요 탭 */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {/* 파이프라인 상태 요약 */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <CogIcon className="h-8 w-8 text-blue-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">활성 파이프라인</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {pipelineStatus.filter(p => p.status === 'running').length}
                  </p>
                </div>
              </div>
            </div>

            {/* 품질 점수 요약 */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <CheckCircleIcon className="h-8 w-8 text-green-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">평균 품질 점수</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {(qualityMetrics.reduce((sum, m) => sum + m.value, 0) / qualityMetrics.length * 100).toFixed(1)}%
                  </p>
                </div>
              </div>
            </div>

            {/* AI 모델 성능 요약 */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <TrendingUpIcon className="h-8 w-8 text-purple-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">평균 AI 정확도</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {(aiModelPerformance.reduce((sum, m) => sum + m.accuracy, 0) / aiModelPerformance.length * 100).toFixed(1)}%
                  </p>
                </div>
              </div>
            </div>

            {/* 품질 이슈 요약 */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <ExclamationCircleIcon className="h-8 w-8 text-red-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">품질 이슈</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {qualityIssues.filter(i => i.severity === 'critical' || i.severity === 'high').length}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 파이프라인 탭 */}
        {activeTab === 'pipeline' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">파이프라인 상태</h2>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {pipelineStatus.map((pipeline, index) => (
                    <div key={index} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(pipeline.status)}`}>
                          {pipeline.status}
                        </div>
                        <div>
                          <h3 className="font-medium text-gray-900">{pipeline.name}</h3>
                          <p className="text-sm text-gray-500">
                            마지막 실행: {formatDate(pipeline.lastRun)}
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-500">처리 시간: {formatDuration(pipeline.duration)}</p>
                        <p className="text-sm text-gray-500">처리된 레코드: {pipeline.recordsProcessed.toLocaleString()}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 품질 탭 */}
        {activeTab === 'quality' && (
          <div className="space-y-6">
            {/* 품질 메트릭 차트 */}
            <div className="bg-white rounded-lg shadow">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">품질 메트릭</h2>
              </div>
              <div className="p-6">
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={qualityMetrics}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" fill="#3B82F6" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* 품질 이슈 */}
            <div className="bg-white rounded-lg shadow">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">품질 이슈</h2>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {qualityIssues.map((issue, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-start justify-between">
                        <div className="flex items-center space-x-3">
                          <div className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(issue.severity)}`}>
                            {issue.severity}
                          </div>
                          <div>
                            <h3 className="font-medium text-gray-900">{issue.category}</h3>
                            <p className="text-sm text-gray-600 mt-1">{issue.description}</p>
                            <p className="text-sm text-gray-500 mt-1">영향받은 레코드: {issue.affectedRecords.toLocaleString()}</p>
                          </div>
                        </div>
                      </div>
                      <div className="mt-3 p-3 bg-blue-50 rounded-md">
                        <p className="text-sm text-blue-800">
                          <strong>권장사항:</strong> {issue.recommendation}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* AI 모델 탭 */}
        {activeTab === 'ai' && (
          <div className="space-y-6">
            {/* AI 모델 성능 차트 */}
            <div className="bg-white rounded-lg shadow">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">AI 모델 성능</h2>
              </div>
              <div className="p-6">
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={aiModelPerformance}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="accuracy" fill="#3B82F6" name="정확도" />
                    <Bar dataKey="precision" fill="#10B981" name="정밀도" />
                    <Bar dataKey="recall" fill="#F59E0B" name="재현율" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* AI 모델 상세 정보 */}
            <div className="bg-white rounded-lg shadow">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">모델 상세 정보</h2>
              </div>
              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {aiModelPerformance.map((model, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                      <h3 className="font-medium text-gray-900 mb-3">{model.name}</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">정확도:</span>
                          <span className="text-sm font-medium">{(model.accuracy * 100).toFixed(1)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">정밀도:</span>
                          <span className="text-sm font-medium">{(model.precision * 100).toFixed(1)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">재현율:</span>
                          <span className="text-sm font-medium">{(model.recall * 100).toFixed(1)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">F1 점수:</span>
                          <span className="text-sm font-medium">{(model.f1Score * 100).toFixed(1)}%</span>
                        </div>
                        <div className="pt-2 border-t border-gray-200">
                          <p className="text-xs text-gray-500">
                            마지막 학습: {formatDate(model.lastTrained)}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 