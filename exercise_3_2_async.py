import httpx
import asyncio
import time

print("=== Task 3.2: Asynchronous HTTP Requests ===")

# Same URLs as sync version
urls = [
    "https://httpbin.org/get?param=1",
    "https://httpbin.org/get?param=2",
    "https://httpbin.org/get?param=3",
    "https://httpbin.org/get?param=4",
    "https://httpbin.org/get?param=5"
]

async def fetch_async(url):
    """Fetch a single URL asynchronously"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

async def main_async():
    """Fetch all URLs asynchronously using asyncio.gather"""
    start_time = time.time()

    print("Starting all requests simultaneously...")

    # asyncio.gather runs all coroutines concurrently
    tasks = [fetch_async(url) for url in urls]
    results = await asyncio.gather(*tasks)

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\n⏱️  Total time: {total_time:.2f} seconds")
    print(f"📊 Average time per request: {total_time/5:.2f} seconds")
    print(f"🚀 Speed improvement: Requests ran concurrently!")

    # Show results
    for i, result in enumerate(results, 1):
        print(f"✓ Got response {i}: {result['args']}")

    return results

if __name__ == "__main__":
    # Run the async function
    results = asyncio.run(main_async())