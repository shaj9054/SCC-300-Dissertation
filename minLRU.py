class LRUCache(object):
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.cache = {}
    
    def get(self, key):
        if key not in self.cache:
            return None
        else:
            value = self.cache[key]
            del self.cache[key]
            self.cache[key] = value
            return value
    
    def put(self, key, value):
        if key in self.cache:
            del self.cache[key]
        elif len(self.cache) >= self.capacity:
            self.cache.popitem()
        self.cache[key] = value