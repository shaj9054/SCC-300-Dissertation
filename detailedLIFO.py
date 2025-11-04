class LifoCache:
    def __init__(self, max_size):
        if max_size < 0:
            self.cache = []
            self.max_size = 0
        else:
            self.cache = []
            self.max_size = max_size

    def get(self, key):
        for i in range(len(self.cache)):
            if self.cache[i][0] == key:
                return self.cache[i][1]
        return None

    def put(self, key, value):
        # Search manually for the key
        for i in range(len(self.cache)):
            if self.cache[i][0] == key:
                # Key already exists, remove existing pair
                del self.cache[i]
                break
        
        # Insert new (key, value) pair at end of list
        self.cache.append((key, value))
        
        # Ensure cache size does not exceed max_size
        if len(self.cache) > self.max_size:
            self.cache.pop()

    def size(self):
        return len(self.cache)