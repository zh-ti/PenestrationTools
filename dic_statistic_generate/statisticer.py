from redis_client import RedisClient
from rich.progress import Progress


class Statisticer:
    redisClient = None
    exceedLen = None

    def __init__(self):
        self.redisClient = RedisClient()

    def statistic(self, filetype, filename):
        self.exceedLen = 0
        with open(filename, 'r', buffering=1024, encoding='utf-8') as file:
            try:
                lines = file.readlines()
                for line in lines:
                    if 0 < len(line) < 64 and not line.isspace():
                        self.redisClient.incrementInHash(filetype, line)
                    else:
                        self.exceedLen += 1
                print(f"{filename} 统计完毕")
            except UnicodeDecodeError:
                pass

    def finish(self):
        self.redisClient.close()
