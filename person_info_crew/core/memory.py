from functools import wraps
from hashlib import sha256
import time

class MemoryCache:
    def __init__(self):
        self.cache = {}
        self.call_counts = {}
        self.ttl = 3600  # 1 hour cache

    def _generate_key(self, func_name, *args, **kwargs):
        sorted_kwargs = tuple(sorted(kwargs.items()))
        key_str = f"{func_name}-{args}-{sorted_kwargs}"
        return sha256(key_str.encode()).hexdigest()

    def cached(self, func, max_calls=50):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = self._generate_key(func.__name__, *args, **kwargs)
            
            # Check rate limits
            if self.call_counts.get(func.__name__, 0) >= max_calls:
                raise ValueError(f"API limit reached for {func.__name__}")
            
            # Check cache
            if key in self.cache and (time.time() - self.cache[key]['timestamp']) < self.ttl:
                return self.cache[key]['data']
            
            # Execute and cache
            result = func(*args, **kwargs)
            self.cache[key] = {
                'data': result,
                'timestamp': time.time()
            }
            self.call_counts[func.__name__] = self.call_counts.get(func.__name__, 0) + 1
            return result
        return wrapper

memory = MemoryCache()