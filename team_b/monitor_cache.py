import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_cache_stats():
    """Monitor Redis cache performance"""
    info = r.info()
    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)
    total = hits + misses
    
    print("\n" + "="*50)
    print("📊 CACHE PERFORMANCE MONITOR")
    print("="*50)
    
    if total > 0:
        hit_ratio = (hits / total) * 100
        print(f"🎯 Hit Ratio: {hit_ratio:.2f}%")
    else:
        print("🎯 Hit Ratio: N/A (no requests yet)")
    
    print(f"✅ Hits: {hits}")
    print(f"❌ Misses: {misses}")
    print(f"📦 Total Keys: {len(r.keys('*'))}")
    print(f"💾 Memory Used: {info['used_memory_human']}")
    
    # Show top 5 cached keys
    keys = r.keys('*')
    if keys:
        print("\n🔑 Sample cached keys:")
        for key in keys[:5]:
            ttl = r.ttl(key)
            print(f"   - {key[:30]}: TTL {ttl}s")

if __name__ == "__main__":
    while True:
        get_cache_stats()
        time.sleep(5)  # Update every 5 seconds
