import json
from pydantic import BaseModel, ValidationError
from typing import Dict, Optional

print("=== Task 2.2: Parse, Modify, and Dump JSON ===")

# Sample JSON string (similar to your get_response.json)
json_string = '''{
    "args": {"name": "alex"},
    "headers": {"Host": "httpbin.org", "Accept": "*/*"},
    "origin": "118.100.221.31",
    "url": "https://httpbin.org/get?name=alex"
}'''

print("Original JSON string:")
print(json_string)

# Parse JSON string into Python dictionary
data = json.loads(json_string)
print("\nParsed into Python dictionary:")
print(data)

# Modify the data
data['origin'] = "192.168.1.1"  # Change the origin
data['args']['name'] = "alex_updated"  # Modify nested data
data['headers']['User-Agent'] = "MyApp/1.0"  # Add new header

print("\nModified dictionary:")
print(data)

# Convert back to formatted JSON string
modified_json = json.dumps(data, indent=2)
print("\nModified JSON with indent=2:")
print(modified_json)

print("\n" + "="*50)
print("=== Task 2.3: Pydantic BaseModel Validation ===")

# Define the same shape using Pydantic BaseModel
class GetResponse(BaseModel):
    args: Dict[str, str]
    headers: Dict[str, str]
    origin: str
    url: str

# Test with valid data
print("\nTesting with VALID data:")
valid_data = {
    "args": {"name": "alex"},
    "headers": {"Host": "httpbin.org", "Accept": "*/*"},
    "origin": "118.100.221.31",
    "url": "https://httpbin.org/get?name=alex"
}

try:
    response = GetResponse(**valid_data)
    print("✅ Valid data accepted!")
    print(f"Response object: {response}")
except ValidationError as e:
    print(f"❌ Validation error: {e}")

# Test with BAD data (missing required fields)
print("\nTesting with BAD data (missing required fields):")
bad_data = {
    "args": {"name": "alex"},
    "headers": {"Host": "httpbin.org"}
    # Missing 'origin' and 'url' - this should fail!
}

try:
    response = GetResponse(**bad_data)
    print("✅ Unexpectedly valid!")
except ValidationError as e:
    print("❌ Validation error (as expected):")
    print(e)

# Test with WRONG data types
print("\nTesting with WRONG data types:")
wrong_type_data = {
    "args": "this should be a dict, not a string",  # Wrong type
    "headers": {"Host": "httpbin.org", "Accept": "*/*"},
    "origin": "118.100.221.31",
    "url": "https://httpbin.org/get?name=alex"
}

try:
    response = GetResponse(**wrong_type_data)
    print("✅ Unexpectedly valid!")
except ValidationError as e:
    print("❌ Validation error (as expected):")
    print(e)