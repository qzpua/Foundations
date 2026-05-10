import httpx
import json
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        # GET request with query parameter
        response = await client.get("https://httpbin.org/get", params={"name": "alex"})
        print("GET Response:")
        print(json.dumps(response.json(), indent=4))
        
        # Save GET response to file
        with open('get_response.json', 'w') as f:
            json.dump(response.json(), f, indent=4)
        
        # POST request with JSON body
        response = await client.post("https://httpbin.org/post", json={"hello": "world"})
        print("\nPOST Response:")
        print(json.dumps(response.json(), indent=4))
        
        # Save POST response to file
        with open('post_response.json', 'w') as f:
            json.dump(response.json(), f, indent=4)

if __name__ == "__main__":
    asyncio.run(main())