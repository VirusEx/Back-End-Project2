import redis

danny = redis.Redis(host='localhost', port=6379, db=0)

print(danny.get('post1'))

def flush(self):
        return self.db.flushdb()