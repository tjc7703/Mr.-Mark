import React from 'react';
import useSWR from 'swr';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { fetchTodayFeed, fetchTrend, fetchAIFeedback } from './api';

export default function Home() {
  const { data: feed } = useSWR('todayFeed', fetchTodayFeed);
  const { data: trend } = useSWR('trend', fetchTrend);
  const { data: aiFeedback } = useSWR('aiFeedback', fetchAIFeedback);

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-3xl font-bold mb-6">Mr. Mark 마케팅 마스터리 대시보드</h1>
      <section className="mb-8 p-4 bg-white rounded shadow">
        <h2 className="text-xl font-semibold mb-2">오늘의 마케팅 소식</h2>
        <ul className="list-disc ml-6 text-gray-700">
          {feed?.news?.map((item: string, i: number) => (
            <li key={i}>{item}</li>
          )) || <li>로딩 중...</li>}
        </ul>
      </section>
      <section className="mb-8 p-4 bg-white rounded shadow">
        <h2 className="text-xl font-semibold mb-2">실시간 트렌드 차트</h2>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={trend?.trends?.map((t: string, i: number) => ({ name: t, value: (i+1)*1000 })) || []}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#2563eb" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </section>
      <section className="mb-8 p-4 bg-white rounded shadow">
        <h2 className="text-xl font-semibold mb-2">미션/체크리스트</h2>
        <ul className="list-disc ml-6 text-gray-700">
          <li>오늘의 실습 미션: 인스타그램 릴스 업로드</li>
          <li>목표 달성 체크: 조회수 3만+</li>
          <li>AI 피드백: {aiFeedback?.feedback || '로딩 중...'}</li>
        </ul>
      </section>
    </main>
  );
} 