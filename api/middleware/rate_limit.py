from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import heapq
from datetime import datetime, timedelta
from collections import defaultdict

# Dictionary to store heaps based on user agent
request_timestamps = defaultdict(list)

# Limit and window size
REQUEST_LIMIT_PER_WINDOW = 1
RATE_LIMIT_WINDOW = timedelta(seconds=60)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user_agent = request.headers.get('User-Agent', 'unknown')
        now = datetime.now()

        if user_agent in request_timestamps:
            if len(request_timestamps[user_agent]) >= REQUEST_LIMIT_PER_WINDOW:
                # Check if the oldest request is within the rate limit window
                if now - request_timestamps[user_agent][0] < RATE_LIMIT_WINDOW:
                    # Too many requests
                    return Response(status_code=429, content="Too Many Requests")
                else:
                    # Remove the oldest timestamp as it's outside the rate limit window
                    heapq.heappop(request_timestamps[user_agent])

        # Add the current request timestamp
        heapq.heappush(request_timestamps[user_agent], now)

        response = await call_next(request)
        return response
