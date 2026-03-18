from locust import HttpUser, task, between, events
import random
import time

# Sample data for Netflix queries
genres = ['Documentaries', 'Dramas', 'Comedies', 'Horror Movies', 'Action', 'Romantic', 'Thrillers']
actors = ['Leonardo DiCaprio', 'Tom Hanks', 'Scarlett Johansson', 'Will Smith', 'Robert Downey Jr.']
years = [2018, 2019, 2020, 2021, 2022, 2023]
countries = ['United States', 'India', 'United Kingdom', 'South Korea']
search_terms = ['love', 'war', 'family', 'school', 'music', 'space']

# Track metrics
cache_hits = 0
cache_misses = 0
total_requests = 0
slow_requests = 0

@events.request.add_listener
def request_handler(request_type, name, response_time, response_length, response, context, exception, **kwargs):
    global cache_hits, cache_misses, total_requests, slow_requests
    total_requests += 1
    
    # Check if response was cached (you'll add this header later)
    if response and response.headers.get('X-Cache') == 'HIT':
        cache_hits += 1
    else:
        cache_misses += 1
    
    # Track slow requests (> 1 second)
    if response_time > 1000:
        slow_requests += 1

@events.test_stop.add_listener
def test_stop_handler(environment, **kwargs):
    print("\n" + "="*60)
    print("📊 FINAL TEST SUMMARY")
    print("="*60)
    print(f"📦 Total Requests: {total_requests}")
    print(f"⚡ Requests/sec: {environment.runner.stats.total.rps:.1f}")
    print(f"✅ Cache Hits: {cache_hits}")
    print(f"❌ Cache Misses: {cache_misses}")
    if total_requests > 0:
        hit_ratio = (cache_hits / total_requests) * 100
        print(f"🎯 Cache Hit Ratio: {hit_ratio:.2f}%")
    print(f"🐢 Slow Requests (>1s): {slow_requests}")
    print(f"📊 95th Percentile: {environment.runner.stats.get('/genre/Dramas', {}).get('avg_response_time', 0):.0f}ms")

class NetflixUser(HttpUser):
    wait_time = between(1, 2.5)
    
    @task(4)
    def browse_genre(self):
        genre = random.choice(genres)
        with self.client.get(f"/genre/{genre}", catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure(f"Slow: {response.elapsed.total_seconds():.2f}s")
    
    @task(3)
    def search_actor(self):
        actor = random.choice(actors)
        self.client.get(f"/actor/{actor}")
    
    @task(2)
    def browse_year(self):
        year = random.choice(years)
        self.client.get(f"/recent/{year}")
    
    @task(1)
    def search_description(self):
        term = random.choice(search_terms)
        self.client.get(f"/search?q={term}")
    
    @task(1)
    def filter_country(self):
        country = random.choice(countries)
        self.client.get(f"/filter?country={country}&type=Movie")