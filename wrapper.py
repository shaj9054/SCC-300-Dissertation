from typing import Any
from TYP import BaseCache
from minLRU import LRUCache
from minFIFO import FifoCache
from minLIFO import LifoCache
from detailedLIFO import LifoCache as DetailedLifoCache
from detailedFIFO import FifoCache as DetailedFifoCache
from detailedLRU import LRUCache as DetailedLRUCache

# Minimal LRU Wrapper
"""
MinimalLRUWrapper

This class serves as a wrapper around a minimal LRU (Least Recently Used) cache implementation.
It extends the BaseCache class and tracks cache hits and misses for performance evaluation.
"""
class MinimalLRUWrapper(BaseCache):
    def __init__(self, max_size: int):
        """
        Initializes a minimal LRU cache wrapper.
        
        Args:
            max_size (int): Maximum size of the cache.
        """
        super().__init__(max_size)
        self.inner_lru = LRUCache(capacity=max_size)

    def get(self, key: str) -> Any:
        """
        Get the value associated with a key from the LRU cache.
        Increments hit or miss counters accordingly.

        Args:
            key (str): The key to look up.

        Returns:
            Any: The value if found, otherwise None.
        """
        result = self.inner_lru.get(key)
        if result is None:
            self.misses += 1
        else:
            self.hits += 1
        return result

    def put(self, key: str, value: Any, size: int) -> None:
        """
        Put a key-value pair into the LRU cache.

        Args:
            key (str): The key to insert.
            value (Any): The value to insert.
            size (int): Size of the object (not used in minimal implementation).
        """
        self.inner_lru.put(key, value)

    def _choose_eviction_victim(self) -> str:
        """
        This method is required by BaseCache but is not used in this wrapper.
        """
        return ""

    def _on_access(self, key: str) -> None:
        """
        Called when a key is accessed. Not implemented for the minimal wrapper.
        """
        pass

    def _on_put(self, key: str) -> None:
        """
        Called when a key is inserted. Not implemented for the minimal wrapper.
        """
        pass

# Minimal FIFO Wrapper
"""
MinimalFifoWrapper

This class serves as a wrapper around a minimal FIFO (First-In-First-Out) cache implementation.
It extends the BaseCache class and tracks cache hits and misses for performance evaluation.
"""
class MinimalFifoWrapper(BaseCache):
    def __init__(self, max_size: int):
        """
        Initializes a minimal FIFO cache wrapper.
        
        Args:
            max_size (int): Maximum size of the cache.
        """
        super().__init__(max_size)
        self.inner_fifo = FifoCache(max_size=max_size)

    def get(self, key: str) -> Any:
        """
        Get the value associated with a key from the FIFO cache.
        Increments hit or miss counters accordingly.

        Args:
            key (str): The key to look up.

        Returns:
            Any: The value if found, otherwise None.
        """
        result = self.inner_fifo.get(key)
        if result is None:
            self.misses += 1
            return None
        else:
            self.hits += 1
            return result

    def put(self, key: str, value: Any, size: int) -> None:
        """
        Put a key-value pair into the FIFO cache.

        Args:
            key (str): The key to insert.
            value (Any): The value to insert.
            size (int): Size of the object (not used in minimal implementation).
        """
        self.inner_fifo.put(key, value)

    def _choose_eviction_victim(self) -> str:
        return ""

    def _on_access(self, key: str) -> None:
        pass

    def _on_put(self, key: str) -> None:
        pass

# Minimal LIFO Wrapper
"""
MinimalLifoWrapper

This class serves as a wrapper around a minimal LIFO (Last-In-First-Out) cache implementation.
It extends the BaseCache class and tracks cache hits and misses for performance evaluation.
"""
class MinimalLifoWrapper(BaseCache):
    def __init__(self, max_size: int):
        super().__init__(max_size)
        self.inner_lifo = LifoCache(capacity=max_size)

    def get(self, key: str) -> Any:
        result = self.inner_lifo.get(key)
        if result is None:
            self.misses += 1
            return None
        else:
            self.hits += 1
            return result

    def put(self, key: str, value: Any, size: int) -> None:
        self.inner_lifo.put(key, value)

    def _choose_eviction_victim(self) -> str:
        return ""

    def _on_access(self, key: str) -> None:
        pass

    def _on_put(self, key: str) -> None:
        pass

# Detailed LIFO Wrapper
"""
DetailedLifoWrapper

This class serves as a wrapper around a detailed LIFO cache implementation.
It extends the BaseCache class and tracks cache hits and misses for performance evaluation.
"""
class DetailedLifoWrapper(BaseCache):
    def __init__(self, max_size: int):
        super().__init__(max_size)
        self.inner_lifo = DetailedLifoCache(max_size=max_size)

    def get(self, key: str) -> Any:
        result = self.inner_lifo.get(key)
        if result is None:
            self.misses += 1
            return None
        else:
            self.hits += 1
            return result

    def put(self, key: str, value: Any, size: int) -> None:
        self.inner_lifo.put(key, value)

    def _choose_eviction_victim(self) -> str:
        return ""

    def _on_access(self, key: str) -> None:
        pass

    def _on_put(self, key: str) -> None:
        pass

# Detailed FIFO Wrapper
"""
DetailedFifoWrapper

This class serves as a wrapper around a detailed FIFO cache implementation.
It extends the BaseCache class and tracks cache hits and misses for performance evaluation.
"""
class DetailedFifoWrapper(BaseCache):
    def __init__(self, max_size: int):
        super().__init__(max_size)
        self.inner_fifo = DetailedFifoCache(capacity=max_size)

    def get(self, key: str) -> Any:
        result = self.inner_fifo.get(key)
        if result is None:
            self.misses += 1
            return None
        else:
            self.hits += 1
            return result

    def put(self, key: str, value: Any, size: int) -> None:
        self.inner_fifo.put(key, value)

    def _choose_eviction_victim(self) -> str:
        return ""

    def _on_access(self, key: str) -> None:
        pass

    def _on_put(self, key: str) -> None:
        pass

# Detailed LRU Wrapper
"""
DetailedLRUWrapper

This class serves as a wrapper around a detailed LRU cache implementation.
It extends the BaseCache class and tracks cache hits and misses for performance evaluation.
"""
class DetailedLRUWrapper(BaseCache):
    def __init__(self, max_size: int):
        super().__init__(max_size)
        self.inner_lru = DetailedLRUCache(capacity=max_size)

    def get(self, key: str) -> Any:
        result = self.inner_lru.get(key)
        if result == -1:
            self.misses += 1
            return None
        else:
            self.hits += 1
            return result

    def put(self, key: str, value: Any, size: int) -> None:
        self.inner_lru.put(key, value)

    def _choose_eviction_victim(self) -> str:
        return ""

    def _on_access(self, key: str) -> None:
        pass

    def _on_put(self, key: str) -> None:
        pass
