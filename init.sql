-- Mr. Mark 데이터베이스 초기화 스크립트

-- 사용자 테이블
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 마케팅 캠페인 테이블
CREATE TABLE IF NOT EXISTS campaigns (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SNS 데이터 테이블
CREATE TABLE IF NOT EXISTS sns_data (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    content TEXT,
    engagement_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI 분석 결과 테이블
CREATE TABLE IF NOT EXISTS ai_analysis (
    id SERIAL PRIMARY KEY,
    content_id INTEGER,
    sentiment_score DECIMAL(3,2),
    engagement_prediction VARCHAR(20),
    recommended_hashtags TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 트렌드 데이터 테이블
CREATE TABLE IF NOT EXISTS trends (
    id SERIAL PRIMARY KEY,
    keyword VARCHAR(100) NOT NULL,
    volume INTEGER,
    growth_rate DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_campaigns_user_id ON campaigns(user_id);
CREATE INDEX IF NOT EXISTS idx_sns_data_platform ON sns_data(platform);
CREATE INDEX IF NOT EXISTS idx_trends_keyword ON trends(keyword);

-- 샘플 데이터 삽입
INSERT INTO users (username, email, password_hash) VALUES
('admin', 'admin@mrmark.com', 'hashed_password_here'),
('demo_user', 'demo@mrmark.com', 'hashed_password_here')
ON CONFLICT (username) DO NOTHING;

INSERT INTO campaigns (user_id, name, description) VALUES
(1, '2024년 마케팅 캠페인', 'AI 기반 마케팅 자동화 캠페인'),
(2, '소셜미디어 전략', '다중 플랫폼 소셜미디어 마케팅')
ON CONFLICT DO NOTHING;

INSERT INTO trends (keyword, volume, growth_rate) VALUES
('AI 마케팅 자동화', 8500, 15.0),
('틱톡 마케팅', 7200, 23.0),
('바이럴 콘텐츠', 6800, 18.0),
('개인화 마케팅', 6100, 12.0),
('메타버스 마케팅', 5400, 8.0)
ON CONFLICT DO NOTHING; 