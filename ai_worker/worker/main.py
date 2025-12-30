from worker.redis_consumer import redis_consumer

def main():
    print("AntiGravity AI Worker (Phase 9.2) starting...")
    redis_consumer.setup()
    redis_consumer.poll()

if __name__ == "__main__":
    main()
