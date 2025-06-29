#!/usr/bin/env python3
"""
Basic GraphQL test for Task 3 requirements
"""

import requests
import json

# GraphQL endpoint
GRAPHQL_URL = "http://127.0.0.1:8000/graphql"

def test_basic_graphql():
    """Test the basic GraphQL endpoint and hello query"""
    print("=== Testing Basic GraphQL Endpoint ===")
    
    # Test 1: Basic hello query
    print("\n1. Testing hello query:")
    query1 = """
    {
        hello
    }
    """
    
    try:
        response = requests.post(GRAPHQL_URL, json={"query": query1})
        response.raise_for_status()
        result = response.json()
        
        print("✓ Hello query result:")
        print(json.dumps(result, indent=2))
        
        # Verify the response
        if result.get('data', {}).get('hello') == 'Hello, GraphQL!':
            print("✅ Hello query working correctly!")
        else:
            print("❌ Hello query not working as expected")
            
    except Exception as e:
        print(f"❌ Error testing hello query: {e}")
    
    # Test 2: Check if GraphiQL interface is accessible
    print("\n2. Testing GraphiQL interface:")
    try:
        response = requests.get(GRAPHQL_URL)
        if response.status_code == 200:
            print("✅ GraphiQL interface is accessible")
        else:
            print(f"❌ GraphiQL interface not accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accessing GraphiQL: {e}")
    
    # Test 3: Test schema introspection
    print("\n3. Testing schema introspection:")
    query3 = """
    {
        __schema {
            types {
                name
            }
        }
    }
    """
    
    try:
        response = requests.post(GRAPHQL_URL, json={"query": query3})
        response.raise_for_status()
        result = response.json()
        
        print("✓ Schema introspection result:")
        print(json.dumps(result, indent=2))
        
        # Check if Query type exists
        types = result.get('data', {}).get('__schema', {}).get('types', [])
        query_type = next((t for t in types if t['name'] == 'Query'), None)
        
        if query_type:
            print("✅ Query type found in schema")
        else:
            print("❌ Query type not found in schema")
            
    except Exception as e:
        print(f"❌ Error testing schema introspection: {e}")

def test_filtering_queries():
    """Test the filtering queries mentioned in Task 3"""
    print("\n=== Testing Task 3 Filtering Queries ===")
    
    # Test 1: Filter customers by name and creation date
    print("\n1. Filter customers by name and creation date:")
    query1 = """
    query {
        allCustomers(filter: { nameIcontains: "Ali", createdAtGte: "2025-01-01" }) {
            edges {
                node {
                    id
                    name
                    email
                    createdAt
                }
            }
        }
    }
    """
    
    try:
        response = requests.post(GRAPHQL_URL, json={"query": query1})
        response.raise_for_status()
        result = response.json()
        
        print("✓ Customer filter result:")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"❌ Error testing customer filter: {e}")
    
    # Test 2: Filter products by price range and sort by stock
    print("\n2. Filter products by price range and sort by stock:")
    query2 = """
    query {
        allProducts(filter: { priceGte: 100, priceLte: 1000 }, orderBy: "-stock") {
            edges {
                node {
                    id
                    name
                    price
                    stock
                }
            }
        }
    }
    """
    
    try:
        response = requests.post(GRAPHQL_URL, json={"query": query2})
        response.raise_for_status()
        result = response.json()
        
        print("✓ Product filter result:")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"❌ Error testing product filter: {e}")
    
    # Test 3: Filter orders by customer name, product name, and total amount
    print("\n3. Filter orders by customer name, product name, and total amount:")
    query3 = """
    query {
        allOrders(filter: { customerName: "Alice", productName: "Laptop", totalAmountGte: 500 }) {
            edges {
                node {
                    id
                    customer {
                        name
                    }
                    totalAmount
                    orderDate
                }
            }
        }
    }
    """
    
    try:
        response = requests.post(GRAPHQL_URL, json={"query": query3})
        response.raise_for_status()
        result = response.json()
        
        print("✓ Order filter result:")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"❌ Error testing order filter: {e}")

if __name__ == "__main__":
    print("Starting Basic GraphQL Tests...")
    print("Make sure the Django server is running on http://127.0.0.1:8000")
    print("=" * 60)
    
    # Test basic GraphQL functionality
    test_basic_graphql()
    
    # Test filtering queries
    test_filtering_queries()
    
    print("\n" + "=" * 60)
    print("Basic GraphQL tests completed!")
    print("\nTo test manually:")
    print("1. Visit: http://127.0.0.1:8000/graphql")
    print("2. Run the query: { hello }")
    print("3. Expected result: { \"data\": { \"hello\": \"Hello, GraphQL!\" } }") 