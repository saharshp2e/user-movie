import redis

class RedisCache:
    def __init__(self, host, port, db):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db)

    def get(self, key):
        return self.redis_client.get(key)

    def setex(self, key, ttl, value):
        self.redis_client.setex(key, ttl, value)

    def delete(self, key):
        self.redis_client.delete(key)
