import redis
from config_holder import ConfigHolder

config = ConfigHolder()


class RedisClient:
    redisClient = None

    def __init__(self):
        self.redisClient = redis.StrictRedis(host=config.redis_host, port=config.redis_port, db=config.redis_db,
                                             username=config.redis_username, password=config.redis_password)

    def set(self, key, value):
        self.redisClient.set(key, value)

    def get(self, key):
        self.redisClient.get(key)

    def setHash(self, name, key, value):
        self.redisClient.hset(name, key, value)

    def getHash(self, name, key):
        self.redisClient.hget(name, key)

    def increment(self, key, num=1):
        self.increment(key, num)

    def decrement(self, key, num=1):
        self.redisClient.decr(key, num)

    def incrementInHash(self, names, key, num=1):
        if len(names) <= 1:
            names.append('other')
        self.redisClient.hincrby(":".join(names), key, num)

    def decrementInHash(self, name, key, num=1):
        self.incrementInHash(name, key, -num)

    def getRedisClient(self):
        return self.redisClient

    def close(self):
        self.redisClient.close()
