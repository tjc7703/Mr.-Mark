import logging
from datetime import datetime

logging.basicConfig(filename='audit.log', level=logging.INFO)

def log_access(user, resource, action):
    logging.info(f"{datetime.now()} | user={user} | resource={resource} | action={action}")

# 예시 사용
log_access('admin', 'model_v1.pkl', 'load')
log_access('user1', 'data/warehouse/sales.csv', 'update') 