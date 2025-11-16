import os
import time
from collections import defaultdict


_rate_limits = os.getenv("RATE_LIMITS", "5")
_window = os.getenv("RATE_LIMIT_WINDOW", "60")  # in seconds
_buckets = defaultdict(list)  # user_id -> list of request timestamps

# sliding window rate limiter
# works for single instance deployments
# for distributed deployments, consider using Redis or similar
# redis-based rate limiter can be implemented later
# redis is a better choice for distributed systems
# redis memory is shared across multiple instances

def allow_request(user_id:str)->bool:
    now = time.time()
    window = _buckets[user_id]
    # Remove timestamps outside the window
    _buckets[user_id] = [t for t in window if now - t < int(_window)]
    if len(_buckets[user_id]) >= int(_rate_limits):
        return False
    _buckets[user_id].append(now)
    return True