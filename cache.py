import json
import redis

HOST = "localhost"
PORT = 6379
DB = 0
TTL = 5  # seconds
NAMESPACE = "sentence:"

client = redis.Redis(host=HOST, port=PORT, db=DB)


class Cache:
    def get(self, key):
        vector = client.get(NAMESPACE + key)
        if vector is not None:
            return json.loads(vector)
        else:
            return None

    def set(self, key, vector):
        client.setex(NAMESPACE + key, TTL, json.dumps(vector))

    def touch(self, key):
        client.expire(NAMESPACE + key, TTL)

    def info(self):
        keys = [
            key.decode().replace(NAMESPACE, "") for key in client.keys(NAMESPACE + "*")
        ]
        info = client.info()

        return {
            "keys": [{"key": key, "ttl": self.ttl(key)} for key in keys],
            "total_cache_size": info["used_memory_human"],
        }

    def ttl(self, key):
        return client.ttl(NAMESPACE + key)
