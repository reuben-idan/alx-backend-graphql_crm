import requests
import json

def test_hello_query():
    url = "http://127.0.0.1:8000/graphql"
    query = """
    {
      hello
    }
    """
    
    payload = {
        "query": query
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'hello' in data['data']:
                result = data['data']['hello']
                print(f"✅ SUCCESS: hello query returned: '{result}'")
                if result == "Hello, GraphQL!":
                    print("✅ ALX Requirement PASSED: hello field returns correct default value")
                else:
                    print(f"❌ ALX Requirement FAILED: Expected 'Hello, GraphQL!' but got '{result}'")
            else:
                print("❌ FAILED: Response does not contain expected data structure")
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ FAILED: Could not connect to server. Make sure Django server is running on http://127.0.0.1:8000/")
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")

if __name__ == "__main__":
    print("Testing ALX GraphQL Endpoint Requirement...")
    print("=" * 50)
    test_hello_query() 