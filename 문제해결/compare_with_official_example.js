const fs = require('fs');
const path = require('path');

function checkFileExists(filePath, label) {
  if (!fs.existsSync(filePath)) {
    console.warn(`❌ ${label} 파일이 존재하지 않습니다: ${filePath}`);
    return false;
  }
  return true;
}

// 1. tailwind.config.js 위치 및 content 경로
const tailwindConfigPath = path.join(__dirname, '../apps/frontend/tailwind.config.js');
if (checkFileExists(tailwindConfigPath, 'tailwind.config.js')) {
  const tailwindConfig = fs.readFileSync(tailwindConfigPath, 'utf-8');
  if (!tailwindConfig.includes('app') || !tailwindConfig.includes('components')) {
    console.warn('❌ tailwind.config.js의 content 경로가 공식 예제와 다릅니다.');
  }
}

// 2. postcss.config.mjs 존재 여부
const postcssConfigPath = path.join(__dirname, '../apps/frontend/postcss.config.mjs');
checkFileExists(postcssConfigPath, 'postcss.config.mjs');

// 3. styles/globals.css 내 Tailwind 지시어
const globalsPath = path.join(__dirname, '../apps/frontend/styles/globals.css');
if (checkFileExists(globalsPath, 'styles/globals.css')) {
  const globals = fs.readFileSync(globalsPath, 'utf-8');
  ['@tailwind base;', '@tailwind components;', '@tailwind utilities;'].forEach(directive => {
    if (!globals.includes(directive)) {
      console.warn(`❌ styles/globals.css에 ${directive}가 공식 예제와 다릅니다.`);
    }
  });
}

// 4. app/layout.tsx에서 글로벌 CSS import
const layoutPath = path.join(__dirname, '../apps/frontend/app/layout.tsx');
if (checkFileExists(layoutPath, 'app/layout.tsx')) {
  const layout = fs.readFileSync(layoutPath, 'utf-8');
  if (!layout.includes("import '../styles/globals.css'")) {
    console.warn('❌ app/layout.tsx에서 글로벌 CSS import가 공식 예제와 다릅니다.');
  }
}

// 5. public 폴더 존재
const publicPath = path.join(__dirname, '../apps/frontend/public');
checkFileExists(publicPath, 'public 폴더');

// 6. package.json 위치 및 Tailwind/Next/PostCSS 버전
const packageJsonPath = path.join(__dirname, '../apps/frontend/package.json');
if (checkFileExists(packageJsonPath, 'package.json')) {
  const pkg = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
  ['tailwindcss', 'next', 'postcss', 'autoprefixer'].forEach(dep => {
    if (!pkg.dependencies?.[dep] && !pkg.devDependencies?.[dep]) {
      console.warn(`❌ package.json에 ${dep}가 공식 예제와 다릅니다.`);
    }
  });
}

console.log('✅ 공식 예제와의 구조/설정 비교 완료. 위 경고가 없으면 구조가 일치합니다.'); 