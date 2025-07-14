const fs = require('fs');
const csv = fs.readFileSync('problem_solution_dataset.csv', 'utf-8');
const lines = csv.split('\n').slice(1);

lines.forEach(line => {
  const [type, detail, cause, prevent, fix] = line.split(',');
  if (type && detail) {
    if (type.includes('API 경로') && !fs.existsSync('openapi.yaml')) {
      console.warn('⚠️ API 명세(OpenAPI) 파일이 없습니다.');
    }
    if (type.includes('정적파일') && !fs.existsSync('public')) {
      console.warn('⚠️ public/ 정적파일 폴더가 없습니다.');
    }
    if (type.includes('환경변수') && !fs.existsSync('.env')) {
      console.warn('⚠️ .env 환경변수 파일이 없습니다.');
    }
  }
}); 