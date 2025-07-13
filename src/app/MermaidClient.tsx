"use client";
import dynamic from 'next/dynamic';
import React from 'react';

const Mermaid = dynamic(() => import('react-mermaid2'), { ssr: false });
 
export default function MermaidClient({ chart }: { chart: string }) {
  return <Mermaid chart={chart} />;
} 