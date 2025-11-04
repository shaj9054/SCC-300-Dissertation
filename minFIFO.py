class FifoCache:
    def __init__(self, max_size):
        self.cache = []
        self.max_size = max_size

    def get(self, key):
        for i in range(len(self.cache)):
            if self.cache[i][0] == key:
                return self.cache[i][1]
        return None

    def put(self, key, value):
        for i in range(len(self.cache)):
            if self.cache[i][0] == key:
                self.cache.pop(i)
                break
        self.cache.insert(0, (key, value))
        if len(self.cache) > self.max_size:
            self.cache.pop()