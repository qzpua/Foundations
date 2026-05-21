import asyncio
import time

print("=== Task 3.3: Blocking vs Non-Blocking in Async Functions ===")

async def blocking_example():
    """This function uses time.sleep() which BLOCKS the event loop"""
    print("🚫 Starting blocking_example() with time.sleep(2)...")
    start = time.time()

    # ❌ WRONG: This blocks the entire event loop!
    # No other async tasks can run while this sleeps
    time.sleep(2)

    end = time.time()
    print(f"🚫 blocking_example() finished after {end-start:.2f} seconds")
    return "blocking result"

async def non_blocking_example():
    """This function uses await asyncio.sleep() which is NON-BLOCKING"""
    print("✅ Starting non_blocking_example() with await asyncio.sleep(2)...")
    start = time.time()

    # ✅ CORRECT: This allows other tasks to run while sleeping
    await asyncio.sleep(2)

    end = time.time()
    print(f"✅ non_blocking_example() finished after {end-start:.2f} seconds")
    return "non-blocking result"

async def demonstrate_blocking():
    """Demonstrate how blocking stalls everything"""
    print("\n" + "="*60)
    print("DEMONSTRATION: Blocking stalls the event loop")
    print("="*60)

    print("\n🔄 Starting both functions simultaneously...")

    # Start both tasks at the same time
    task1 = asyncio.create_task(blocking_example())
    task2 = asyncio.create_task(non_blocking_example())

    start_time = time.time()

    # Wait for both to complete
    results = await asyncio.gather(task1, task2)

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\n⏱️  Total time for both tasks: {total_time:.2f} seconds")
    print("📊 Notice how the blocking task made everything take longer!")
    print("   The non-blocking task had to wait for the blocking one to finish.")

    return results

async def demonstrate_non_blocking():
    """Demonstrate how non-blocking allows concurrency"""
    print("\n" + "="*60)
    print("DEMONSTRATION: Non-blocking allows concurrency")
    print("="*60)

    async def quick_task(name):
        print(f"⚡ {name} starting...")
        await asyncio.sleep(0.5)  # Fast async sleep
        print(f"⚡ {name} finished!")
        return f"{name} result"

    print("\n🔄 Starting 3 quick tasks simultaneously...")

    start_time = time.time()

    # All 3 tasks run concurrently (total ~0.5s instead of ~1.5s)
    tasks = [
        quick_task("Task A"),
        quick_task("Task B"),
        quick_task("Task C")
    ]

    results = await asyncio.gather(*tasks)

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\n⏱️  Total time for 3 concurrent tasks: {total_time:.2f} seconds")
    print("📊 All tasks finished in ~0.5s instead of ~1.5s!")
    print("   This is why async programming is powerful for I/O operations.")

    return results

async def main():
    """Run all demonstrations"""
    print("Understanding Async Blocking - Why 'Don't Block the Event Loop' Matters")
    print("="*70)

    # First demonstration: blocking behavior
    await demonstrate_blocking()

    # Second demonstration: non-blocking concurrency
    await demonstrate_non_blocking()

    print("\n" + "="*70)
    print("KEY LESSONS:")
    print("1. 🚫 time.sleep() BLOCKS the event loop - nothing else can run")
    print("2. ✅ await asyncio.sleep() is NON-BLOCKING - other tasks can run")
    print("3. 🔄 HTTP requests are I/O operations - async makes them concurrent")
    print("4. 📈 Blocking defeats the purpose of async programming")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())