import redis
from datetime import timedelta
from config.config import RATELIMIT_STORAGE_URI

ACCESS_EXPIRES = timedelta(hours=1)

jwt_redis_blocklist = redis.StrictRedis.from_url(url=RATELIMIT_STORAGE_URI)
# (host="localhost", port=6379, db=0, decode_responses=True)

