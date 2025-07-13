import logging
from prometheus_client import Counter, start_http_server
import time

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('mrmark-monitoring')

# 메트릭 예시
REQUEST_COUNT = Counter('mrmark_requests_total', '총 요청 수')
ERROR_COUNT = Counter('mrmark_errors_total', '에러 수')

if __name__ == '__main__':
    start_http_server(8001)
    logger.info('Prometheus 메트릭 서버 시작 (8001 포트)')
    while True:
        REQUEST_COUNT.inc()
        time.sleep(5) 