import json
from datetime import datetime

# KPI/피드백/실험 데이터 예시 로드
with open(
    "reports/kpi_report_{}.txt".format(datetime.now().strftime("%Y%m%d")), "r"
) as f:
    kpi = json.load(f)

# 개선 포인트 추출 예시
improvements = []
if kpi["api_error_rate"] > 0.01:
    improvements.append("API 에러율이 높음: 에러 핸들링/테스트 강화 필요")
if kpi["avg_response_time"] > 0.5:
    improvements.append("응답 속도 개선 필요: 인프라/코드 최적화")
if kpi["feedback_score"] < 4.0:
    improvements.append("사용자 만족도 개선 필요: 피드백 분석 및 UX 개선")

print(
    json.dumps(
        {"date": kpi["date"], "improvement_suggestions": improvements},
        ensure_ascii=False,
        indent=2,
    )
)
