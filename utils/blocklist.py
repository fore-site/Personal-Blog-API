import redis
from datetime import timedelta

ACCESS_EXPIRES = timedelta(hours=1)

jwt_redis_blocklist = redis.StrictRedis.from_url(url="redis://red-d3ipkrbe5dus739aui50:6379")
# (host="localhost", port=6379, db=0, decode_responses=True)

