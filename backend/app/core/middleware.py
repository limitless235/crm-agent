from fastapi import Request, HTTPException, status
import time
from app.core.config import settings
import redis

# Rate limit: 1000 requests per minute
RATE_LIMIT = 1000
WINDOW = 60

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

async def rate_limit_middleware(request: Request, call_next):
    # Only rate limit API calls
    if not request.url.path.startswith(settings.API_V1_STR):
        return await call_next(request)

    # Get client IP or user ID if authenticated
    # For now, use IP for simplicity
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"
    
    current_time = int(time.time())
    
    # Use Redis to store timestamps of requests
    # Use a unique ID (timestamp + counter or uuid) to ensure every request is counted
    request_id = f"{current_time}:{time.time_ns()}"
    
    pipe = redis_client.pipeline()
    pipe.zremrangebyscore(key, 0, current_time - WINDOW)
    pipe.zadd(key, {request_id: current_time})
    pipe.zcard(key)
    pipe.expire(key, WINDOW)
    results = pipe.execute()
    
    request_count = results[2]
    
    if request_count > RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later."
        )
        
    response = await call_next(request)
    return response
