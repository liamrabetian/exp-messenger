from uuid import uuid4

from redis import StrictRedis
from nameko.extensions import DependencyProvider


class RedisError(Exception):
    pass



class RedisClient:
    def __init__(self, url):
        self.redis = StrictRedis.from_url(
            url, decode_responses=True
        )

    def get_message(self, message_id: int) -> str:
        message = self.redis.get(message_id)

        if message is None:
            raise RedisError(f'Message Not Found: {message_id}')
        
        return message
    
    def save_message(self, message):
        message_id = uuid4().hex
        self.redis.set(message_id, message)

        return message_id


class MessageStore(DependencyProvider):
    def setup(self):
        redis_url = self.container.config['REDIS_URL']
        self.client = RedisClient(redis_url)
    
    def stop(self):
        del self.client
    
    def get_dependency(self, worker_ctx):
        return self.client
