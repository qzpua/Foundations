import httpx
import json
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        # 404 Not Found
        try:
            response = await client.get("https://httpbin.org/status/404")
            print(f"404 Response Status: {response.status_code}")
            print("Response Text:", response.text)
        except Exception as e:
            print("Error:", e)
        
        # 500 Internal Server Error
        try:
            response = await client.get("https://httpbin.org/status/500")
            print(f"\n500 Response Status: {response.status_code}")
            print("Response Text:", response.text)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())