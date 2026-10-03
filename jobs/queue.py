import os

import redis
from rq import Queue

redis_connection = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
queue = Queue("notifications", connection=redis_connection)
