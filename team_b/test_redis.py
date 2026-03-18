print("Creating test file") 
import redis
import time

print("🔍 Testing Redis connection...")
print("-" * 40)

try:
    # Connect to Redis
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    # Test connection
    r.ping()
    print("✅ Connected to Redis successfully!")
    
    # Test set/get
    r.set('test_key', 'Hello Team B!')
    value = r.get('test_key')
    print(f"✅ Retrieved: {value}")
    
    # Get Redis info
    info = r.info()
    print(f"\n📊 Redis Stats:")
    print(f"   Version: {info['redis_version']}")
    print(f"   Memory used: {info['used_memory_human']}")
    
    # Count keys
    if 'db0' in info:
        print(f"   Total keys: {info['db0']['keys']}")
    
    print("\n✨ All tests passed! Your setup is ready!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n🔧 Troubleshooting:")
    print("1. Is Docker running? Check system tray for whale icon")
    print("2. Run: docker ps (should show redis-server)")
    print("3. Run: docker start redis-server")
    print("4. Check if Redis is on correct port: docker logs redis-server")