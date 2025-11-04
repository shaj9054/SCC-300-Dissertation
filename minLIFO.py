class LifoCache:
    def __init__(self, capacity=None):
        self.queue = []
        self.capacity = capacity

    def get(self, key):
        for item in reversed(self.queue):
            if item[0] == key:
                return item[1]
        return None

    def put(self, key, value):
        if self.capacity is not None and len(self.queue) >= self.capacity:
            self.queue.pop()
        self.queue.append((key, value))

    def size(self):
        return len(self.queue)