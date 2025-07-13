import React from 'react';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-3xl font-bold mb-6">Mr. Mark 마케팅 마스터리 대시보드</h1>
      <section className="mb-8 p-4 bg-white rounded shadow">
        <h2 className="text-xl font-semibold mb-2">오늘의 마케팅 소식</h2>
        <div className="text-gray-600">실시간 뉴스, 트렌드, 인기 콘텐츠 등 표시</div>
      </section>
      <section className="mb-8 p-4 bg-white rounded shadow">
        <h2 className="text-xl font-semibold mb-2">실시간 트렌드 차트</h2>
        <div className="text-gray-600">Recharts/Chart.js로 트렌드 시각화</div>
      </section>
      <section className="mb-8 p-4 bg-white rounded shadow">
        <h2 className="text-xl font-semibold mb-2">마케팅 마인드맵</h2>
        <div className="text-gray-600">React Flow/Mermaid로 마인드맵 시각화</div>
      </section>
      <section className="mb-8 p-4 bg-white rounded shadow">
        <h2 className="text-xl font-semibold mb-2">미션/체크리스트</h2>
        <ul className="list-disc ml-6 text-gray-700">
          <li>오늘의 실습 미션</li>
          <li>목표 달성 체크</li>
          <li>AI 피드백</li>
        </ul>
      </section>
    </main>
  );
} 