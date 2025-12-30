import redis
import sys
from worker.settings import settings

def check_health():
    try:
        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        if r.ping():
            print("Worker healthy: Redis connected.")
            sys.exit(0)
    except Exception as e:
        print(f"Worker unhealthy: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_health()
