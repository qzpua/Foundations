import httpx
import time

print("=== Task 3.1: Synchronous HTTP Requests ===")

# List of URLs to fetch (using httpbin.org for testing)
urls = [
    "https://httpbin.org/get?param=1",
    "https://httpbin.org/get?param=2",
    "https://httpbin.org/get?param=3",
    "https://httpbin.org/get?param=4",
    "https://httpbin.org/get?param=5"
]

def fetch_sync(url):
    """Fetch a single URL synchronously"""
    response = httpx.get(url)
    return response.json()

def main_sync():
    """Fetch all URLs synchronously in a loop"""
    start_time = time.time()

    results = []
    for url in urls:
        print(f"Fetching {url}...")
        result = fetch_sync(url)
        results.append(result)
        print(f"✓ Got response from {url.split('?')[1]}")

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\n⏱️  Total time: {total_time:.2f} seconds")
    print(f"📊 Average time per request: {total_time/5:.2f} seconds")
    return results

if __name__ == "__main__":
    results = main_sync()