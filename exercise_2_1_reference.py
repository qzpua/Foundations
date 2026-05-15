# Task 2.1: JSON Structure Diagrams
# This file contains the JSON structures you need to draw on paper
# Use boxes for objects {} and lists for arrays []

import json

# JSON 1: GET Response Structure
get_response = {
    "args": {
        "name": "alex"
    },
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Host": "httpbin.org",
        "User-Agent": "python-httpx/0.28.1",
        "X-Amzn-Trace-Id": "Root=1-6a008dea-77cb98bc6c5662183fc231d8"
    },
    "origin": "118.100.221.31",
    "url": "https://httpbin.org/get?name=alex"
}

# JSON 2: POST Response Structure
post_response = {
    "args": {},
    "data": "{\"hello\":\"world\"}",
    "files": {},
    "form": {},
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Content-Length": "17",
        "Content-Type": "application/json",
        "Host": "httpbin.org",
        "User-Agent": "python-httpx/0.28.1",
        "X-Amzn-Trace-Id": "Root=1-6a008deb-754aea4d0aa6a97618cfe92b"
    },
    "json": {
        "hello": "world"
    },
    "origin": "118.100.221.31",
    "url": "https://httpbin.org/post"
}

# JSON 3: Simple Example Structure (for practice)
simple_example = {
    "user": {
        "name": "John Doe",
        "age": 30,
        "active": True
    },
    "preferences": ["dark_mode", "notifications", "auto_save"],
    "metadata": {
        "created_at": "2024-01-15",
        "version": 1.2
    }
}

print("=== JSON Structures for Paper Diagrams ===")
print("\n1. GET Response Structure:")
print(json.dumps(get_response, indent=2))

print("\n2. POST Response Structure:")
print(json.dumps(post_response, indent=2))

print("\n3. Simple Example Structure:")
print(json.dumps(simple_example, indent=2))

print("\n" + "="*50)
print("DRAWING GUIDE:")
print("• Objects {} → Draw as BOXES/RECTANGLES")
print("• Arrays [] → Draw as BULLET POINT LISTS")
print("• Primitives (strings, numbers, booleans) → Plain text")
print("• Nested objects → Indented boxes inside boxes")
print("• Label all keys clearly")