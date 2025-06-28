import redis

ACCESS_EXPIRES = timedelta(hours=1)

jwt_redis_blocklist = redis.StrictRedis(host="localhost", port=5000, db=0, decode_responses=True)