import requests

def test_hello():
    url = "http://localhost:8000/graphql"
    query = """
    query {
        hello
    }
    """
    
    response = requests.post(url, json={"query": query})
    print("Hello query result:", response.json())

if __name__ == "__main__":
    test_hello() 