# Next.js + TailwindCSS 스타일 미적용 근본 원인 진단 및 해결 가이드

## 1. 핵심 점검 체크리스트
- [ ] layout.tsx에서 글로벌 CSS import (`import '../styles/globals.css'`)
- [ ] tailwind.config.js의 content 경로가 app, src, components, pages 등 전체를 포함하는지
- [ ] styles/globals.css에 TailwindCSS 지시어(`@tailwind base;`, `@tailwind components;`, `@tailwind utilities;`)가 포함되어 있는지
- [ ] .next/static/css/에 Tailwind 유틸리티 클래스가 실제로 포함되어 있는지
- [ ] 브라우저 네트워크 탭에서 CSS 파일이 정상적으로 로드되는지(200 OK)
- [ ] Dockerfile/배포 스크립트에서 styles, tailwind.config.js, postcss.config.mjs, public 폴더가 누락 없이 복사되는지
- [ ] Tailwind, PostCSS, Next.js 버전 호환성 확인

## 2. 자동화 진단 스크립트 예시 (Node.js)
```js
const fs = require('fs');
const path = require('path');

// 1. layout.tsx에서 글로벌 CSS import 확인
const layoutPath = path.join(__dirname, '../apps/frontend/app/layout.tsx');
const layout = fs.readFileSync(layoutPath, 'utf-8');
if (!layout.includes("import '../styles/globals.css'")) {
  console.warn('❌ layout.tsx에서 글로벌 CSS import가 누락되었습니다.');
}

// 2. tailwind.config.js content 경로 확인
const tailwindConfigPath = path.join(__dirname, '../apps/frontend/tailwind.config.js');
const tailwindConfig = fs.readFileSync(tailwindConfigPath, 'utf-8');
if (!tailwindConfig.includes('app') || !tailwindConfig.includes('components')) {
  console.warn('❌ tailwind.config.js의 content 경로가 충분히 포괄적이지 않습니다.');
}

// 3. globals.css에 TailwindCSS 지시어 확인
const globalsPath = path.join(__dirname, '../apps/frontend/styles/globals.css');
const globals = fs.readFileSync(globalsPath, 'utf-8');
['@tailwind base;', '@tailwind components;', '@tailwind utilities;'].forEach(directive => {
  if (!globals.includes(directive)) {
    console.warn(`❌ globals.css에 ${directive}가 누락되었습니다.`);
  }
});

// 4. .next/static/css/에 Tailwind 유틸리티 포함 여부(샘플)
const nextCssDir = path.join(__dirname, '../apps/frontend/.next/static/css');
if (fs.existsSync(nextCssDir)) {
  const cssFiles = fs.readdirSync(nextCssDir);
  let found = false;
  cssFiles.forEach(file => {
    const css = fs.readFileSync(path.join(nextCssDir, file), 'utf-8');
    if (css.includes('bg-neon-blue') || css.includes('text-hero')) found = true;
  });
  if (!found) {
    console.warn('❌ .next/static/css/에 Tailwind 유틸리티 클래스가 포함되어 있지 않습니다.');
  }
}

console.log('✅ 진단 완료. 위 경고가 없으면 TailwindCSS가 정상 적용됩니다.');
```

## 3. 공식 예제와 동일한 최소 구조로 테스트 권장
- https://github.com/vercel/next.js/tree/canary/examples/with-tailwindcss

## 4. 추가로 점검해야 할 사항
- 브라우저 캐시 완전 삭제 후 강력 새로고침
- Next.js, TailwindCSS, PostCSS, Autoprefixer 버전 호환성 재설치
- public 폴더 및 정적 파일 존재 확인
- 배포 환경(Docker 등)에서 정적 파일, 스타일, 설정 파일 복사 누락 없는지 확인 