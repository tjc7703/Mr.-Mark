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
    const filePath = path.join(nextCssDir, file);
    if (fs.statSync(filePath).isFile()) {
      const css = fs.readFileSync(filePath, 'utf-8');
      if (css.includes('bg-neon-blue') || css.includes('text-hero')) found = true;
    }
  });
  if (!found) {
    console.warn('❌ .next/static/css/에 Tailwind 유틸리티 클래스가 포함되어 있지 않습니다.');
  }
}

console.log('✅ 진단 완료. 위 경고가 없으면 TailwindCSS가 정상 적용됩니다.'); 