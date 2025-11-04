from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            # Move the key to the end of the cache
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        else:
            # If the key is not found, return -1
            return -1

    def put(self, key, value):
        if len(self.cache) >= self.capacity:
            # Remove the oldest key if the cache is full
            self.cache.popitem(last=False)
        # Add a new key-value pair to the cache
        self.cache[key] = value

    def size(self):
        return len(self.cache)