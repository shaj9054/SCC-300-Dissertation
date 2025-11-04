from collections import deque

class FifoCache:
    """A simple FIFO cache."""
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.keys = deque()
        
    def put(self, key, value):
        """Add a new key-value pair to the cache."""
        if len(self.keys) == self.capacity:
            oldest_key = self.keys.popleft()
            del self.cache[oldest_key]
        self.cache[key] = value
        self.keys.append(key)
    
    def get(self, key):
        """Return the value associated with the given key, or None if not found."""
        return self.cache.get(key)
    
    def size(self):
        """Return the number of elements in the cache."""
        return len(self.keys)