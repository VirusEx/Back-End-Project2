import redis

like = redis.Redis(host='localhost', port=6379, db=0)

like.incr('post1')
like.incr('post2')
like.incr('tryme')
print(like.get('tryme'))