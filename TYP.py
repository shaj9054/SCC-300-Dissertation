from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Any, Dict, List, Tuple
import time
import random
import statistics
from functools import partial

# Each item in our cache needs to store several pieces of information
class CacheItem:
    """
    Represents a single item in the cache.
    - A label (key)
    - Contents (value)
    - Size (how much space it takes)
    """
    def __init__(self, key: str, value: Any, size: int):
        self.key = key          # Unique identifier for the item
        self.value = value      # The actual data we're storing
        self.size = size        # How much space this item takes in the cache

# Base class that defines what every cache must be able to do
class BaseCache(ABC):
    """
    Abstract base class for all cache implementations.
    """
    def __init__(self, max_size: int):
        self.max_size = max_size        # Maximum space available in the cache
        self.current_size = 0           # How much space is currently used
        self.hits = 0                   # Number of successful cache retrievals
        self.misses = 0                 # Number of failed cache retrievals
        self.items: Dict[str, CacheItem] = {}  # Storage for cached items
    
    def get(self, key: str) -> Any:
        """
        Try to retrieve an item from the cache.
        - If you find it (hit)
        - If you don't (miss)
        """
        if key in self.items:
            self.hits += 1
            self._on_access(key)
            return self.items[key].value
        self.misses += 1
        return None
    
    def put(self, key: str, value: Any, size: int) -> None:
        """
        Add or update an item in the cache.
        If the cache is full, we need to remove something first (eviction).
        """
        if size > self.max_size:
            raise ValueError(f"Item size {size} exceeds cache max size {self.max_size}")
        
        if key in self.items:
            self._remove_item(key)
        
        while self.current_size + size > self.max_size and self.items:
            evicted_key = self._choose_eviction_victim()
            if evicted_key:
                self._remove_item(evicted_key)
        
        self.items[key] = CacheItem(key, value, size)
        self.current_size += size
        self._on_put(key)
    
    def _remove_item(self, key: str) -> None:
        """
        Helper method to remove an item from the cache and update the size.
        """
        if key in self.items:
            self.current_size -= self.items[key].size
            del self.items[key]
    
    def get_hit_ratio(self) -> float:
        """
        Calculate how effective our cache is being.
        Hit ratio = (number of hits) / (total number of lookups)
        """
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0
    
    @abstractmethod
    def _choose_eviction_victim(self) -> str:
        pass
    
    @abstractmethod
    def _on_access(self, key: str) -> None:
        pass
    
    @abstractmethod
    def _on_put(self, key: str) -> None:
        pass

class LIFOCache(BaseCache):
    """
    LIFO Cache removes the most recently added item when space is needed.
    """
    def __init__(self, max_size: int):
        super().__init__(max_size)
        self.insertion_order: List[str] = []
    
    def _choose_eviction_victim(self) -> str:
        while self.insertion_order and self.insertion_order[-1] not in self.items:
            self.insertion_order.pop()
        return self.insertion_order.pop() if self.insertion_order else None
    
    def _on_access(self, key: str) -> None:
        pass
    
    def _on_put(self, key: str) -> None:
        if key in self.insertion_order:
            self.insertion_order.remove(key)
        self.insertion_order.append(key)
    
    def _remove_item(self, key: str) -> None:
        super()._remove_item(key)
        if key in self.insertion_order:
            self.insertion_order.remove(key)

class FIFOCache(BaseCache):
    """
    FIFO Cache removes the oldest item when space is needed.
    """
    def __init__(self, max_size: int):
        super().__init__(max_size)
        self.insertion_order: List[str] = []
    
    def _choose_eviction_victim(self) -> str:
        while self.insertion_order and self.insertion_order[0] not in self.items:
            self.insertion_order.pop(0)
        return self.insertion_order.pop(0) if self.insertion_order else None
    
    def _on_access(self, key: str) -> None:
        pass
    
    def _on_put(self, key: str) -> None:
        if key in self.insertion_order:
            self.insertion_order.remove(key)
        self.insertion_order.append(key)
    
    def _remove_item(self, key: str) -> None:
        super()._remove_item(key)
        if key in self.insertion_order:
            self.insertion_order.remove(key)

class LRUCache(BaseCache):
    """
    LRU Cache removes the item that hasn't been accessed for the longest time.
    """
    def __init__(self, max_size: int):
        super().__init__(max_size)
        self.access_order = OrderedDict()
    
    def _choose_eviction_victim(self) -> str:
        while self.access_order and next(iter(self.access_order)) not in self.items:
            self.access_order.popitem(last=False)
        return next(iter(self.access_order)) if self.access_order else None
    
    def _on_access(self, key: str) -> None:
        if key in self.access_order:
            del self.access_order[key]
        self.access_order[key] = None
    
    def _on_put(self, key: str) -> None:
        if key in self.access_order:
            del self.access_order[key]
        self.access_order[key] = None
    
    def _remove_item(self, key: str) -> None:
        super()._remove_item(key)
        if key in self.access_order:
            del self.access_order[key]

def test_cache_performance(cache: BaseCache, access_sequence: List[Tuple[str, Any, int]]) -> float:
    """
    Test how well a cache performs with a given sequence of accesses.
    Returns the hit ratio (successful gets / total gets).
    """
    for key, value, size in access_sequence:
        result = cache.get(key)
        if result is None:
            cache.put(key, value, size)
    return cache.get_hit_ratio()

# Functions to create different types of test sequences

def create_cyclic_sequence(n_items: int, cycle_length: int, item_size: int = 1) -> List[Tuple[str, Any, int]]:
    """
    Creates a repeating sequence of accesses.
    Example: [A,B,C,A,B,C,A,B,C] for n_items=3
    """
    sequence = []
    for i in range(n_items):
        key = f"item_{i}"
        sequence.append((key, f"value_{i}", item_size))
    
    for i in range(n_items, cycle_length):
        key = f"item_{i % n_items}"
        sequence.append((key, f"value_{i}", item_size))
    return sequence

def create_random_sequence(n_items: int, sequence_length: int, item_size: int = 1) -> List[Tuple[str, Any, int]]:
    """
    Creates a sequence with random accesses.
    """
    sequence = []
    for i in range(n_items):
        key = f"item_{i}"
        sequence.append((key, f"value_{i}", item_size))
    
    for i in range(n_items, sequence_length):
        key = f"item_{random.randint(0, n_items-1)}"
        sequence.append((key, f"value_{i}", item_size))
    return sequence

def create_locality_sequence(n_items: int, sequence_length: int, locality_window: int, item_size: int = 1) -> List[Tuple[str, Any, int]]:
    """
    Creates a sequence with temporal locality (items accessed recently are 
    likely to be accessed again soon).
    """
    sequence = []
    for i in range(n_items):
        key = f"item_{i}"
        sequence.append((key, f"value_{i}", item_size))
    
    current_window = []
    for i in range(n_items, sequence_length):
        if i % locality_window == 0 or not current_window:
            window_size = min(n_items, 3)
            current_window = random.sample([f"item_{j}" for j in range(n_items)], window_size)
        
        key = random.choice(current_window)
        sequence.append((key, f"value_{i}", item_size))
    return sequence

def multiple_run_test(
    cache_class,
    sequence_func,
    n_items: int,
    sequence_length: int,
    runs: int = 10,
    cache_size: int = 3
) -> float:
    """
    Runs the same cache on newly generated sequences multiple times.
    Returns the average hit ratio.
    """
    hit_ratios = []
    for _ in range(runs):
        sequence = sequence_func(n_items, sequence_length)
        cache = cache_class(cache_size)
        ratio = test_cache_performance(cache, sequence)
        hit_ratios.append(ratio)
    return statistics.mean(hit_ratios)

SEQUENCES = {
    "cyclic": partial(create_cyclic_sequence, item_size=1),
    "random": partial(create_random_sequence, item_size=1),
    "locality": partial(create_locality_sequence, locality_window=4, item_size=1),
}

CACHES = {
    "LIFO": LIFOCache,
    "FIFO": FIFOCache,
    "LRU": LRUCache,
}

if __name__ == "__main__":
    n_items = 6
    sequence_length = 20
    runs = 10
    cache_size = 3

    for seq_name, seq_func in SEQUENCES.items():
        print(f"\nTesting '{seq_name}' sequence with {runs} runs each:")
        for cache_name, cache_class in CACHES.items():
            avg_ratio = multiple_run_test(
                cache_class=cache_class,
                sequence_func=seq_func,
                n_items=n_items,
                sequence_length=sequence_length,
                runs=runs,
                cache_size=cache_size
            )
            print(
                f"{cache_name} "
                f"Average Hit Ratio: {avg_ratio:.2%}"
            )
