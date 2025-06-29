#!/usr/bin/env python3
"""
Test script for GraphQL filtering functionality
"""

import requests
import json
from datetime import datetime, timedelta

# GraphQL endpoint
GRAPHQL_URL = "http://127.0.0.1:8000/graphql"

def execute_query(query, variables=None):
    """Execute a GraphQL query"""
    payload = {
        "query": query,
        "variables": variables or {}
    }
    
    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error executing query: {e}")
        return None

def test_customer_filters():
    """Test customer filtering functionality"""
    print("=== Testing Customer Filters ===")
    
    # Test 1: Filter customers by name
    query1 = """
    query {
        filteredCustomers(filter: { nameIcontains: "Ali" }) {
            id
            name
            email
            phone
            createdAt
        }
    }
    """
    
    result1 = execute_query(query1)
    if result1:
        print("✓ Filter by name (icontains):")
        print(json.dumps(result1, indent=2))
    
    # Test 2: Filter customers by email
    query2 = """
    query {
        filteredCustomers(filter: { emailIcontains: "alice" }) {
            id
            name
            email
            phone
            createdAt
        }
    }
    """
    
    result2 = execute_query(query2)
    if result2:
        print("\n✓ Filter by email (icontains):")
        print(json.dumps(result2, indent=2))
    
    # Test 3: Filter customers by phone pattern
    query3 = """
    query {
        filteredCustomers(filter: { phonePattern: "+1" }) {
            id
            name
            email
            phone
            createdAt
        }
    }
    """
    
    result3 = execute_query(query3)
    if result3:
        print("\n✓ Filter by phone pattern:")
        print(json.dumps(result3, indent=2))
    
    # Test 4: Filter customers by creation date
    query4 = """
    query {
        filteredCustomers(filter: { createdAtGte: "2025-01-01T00:00:00Z" }) {
            id
            name
            email
            phone
            createdAt
        }
    }
    """
    
    result4 = execute_query(query4)
    if result4:
        print("\n✓ Filter by creation date:")
        print(json.dumps(result4, indent=2))

def test_product_filters():
    """Test product filtering functionality"""
    print("\n=== Testing Product Filters ===")
    
    # Test 1: Filter products by price range
    query1 = """
    query {
        filteredProducts(filter: { priceGte: 100, priceLte: 1000 }) {
            id
            name
            price
            stock
        }
    }
    """
    
    result1 = execute_query(query1)
    if result1:
        print("✓ Filter by price range:")
        print(json.dumps(result1, indent=2))
    
    # Test 2: Filter products by stock
    query2 = """
    query {
        filteredProducts(filter: { stockGte: 5 }) {
            id
            name
            price
            stock
        }
    }
    """
    
    result2 = execute_query(query2)
    if result2:
        print("\n✓ Filter by stock (gte):")
        print(json.dumps(result2, indent=2))
    
    # Test 3: Filter products with low stock
    query3 = """
    query {
        filteredProducts(filter: { lowStock: true }) {
            id
            name
            price
            stock
        }
    }
    """
    
    result3 = execute_query(query3)
    if result3:
        print("\n✓ Filter by low stock:")
        print(json.dumps(result3, indent=2))
    
    # Test 4: Filter products by name and sort by price
    query4 = """
    query {
        filteredProducts(filter: { nameIcontains: "Laptop", orderBy: "price" }) {
            id
            name
            price
            stock
        }
    }
    """
    
    result4 = execute_query(query4)
    if result4:
        print("\n✓ Filter by name and sort by price:")
        print(json.dumps(result4, indent=2))

def test_order_filters():
    """Test order filtering functionality"""
    print("\n=== Testing Order Filters ===")
    
    # Test 1: Filter orders by total amount
    query1 = """
    query {
        filteredOrders(filter: { totalAmountGte: 500 }) {
            id
            totalAmount
            orderDate
            customer {
                name
                email
            }
            items {
                product {
                    name
                    price
                }
                unitPrice
            }
        }
    }
    """
    
    result1 = execute_query(query1)
    if result1:
        print("✓ Filter by total amount:")
        print(json.dumps(result1, indent=2))
    
    # Test 2: Filter orders by customer name
    query2 = """
    query {
        filteredOrders(filter: { customerName: "Alice" }) {
            id
            totalAmount
            orderDate
            customer {
                name
                email
            }
        }
    }
    """
    
    result2 = execute_query(query2)
    if result2:
        print("\n✓ Filter by customer name:")
        print(json.dumps(result2, indent=2))
    
    # Test 3: Filter orders by product name
    query3 = """
    query {
        filteredOrders(filter: { productName: "Laptop" }) {
            id
            totalAmount
            orderDate
            customer {
                name
            }
            items {
                product {
                    name
                    price
                }
            }
        }
    }
    """
    
    result3 = execute_query(query3)
    if result3:
        print("\n✓ Filter by product name:")
        print(json.dumps(result3, indent=2))
    
    # Test 4: Filter orders by date range
    query4 = """
    query {
        filteredOrders(filter: { orderDateGte: "2025-01-01T00:00:00Z" }) {
            id
            totalAmount
            orderDate
            customer {
                name
            }
        }
    }
    """
    
    result4 = execute_query(query4)
    if result4:
        print("\n✓ Filter by order date:")
        print(json.dumps(result4, indent=2))

def test_relay_connections():
    """Test Relay connection filtering"""
    print("\n=== Testing Relay Connections ===")
    
    # Test 1: All customers with Relay connection
    query1 = """
    query {
        allCustomers {
            edges {
                node {
                    id
                    name
                    email
                    phone
                    createdAt
                }
            }
            pageInfo {
                hasNextPage
                hasPreviousPage
                startCursor
                endCursor
            }
        }
    }
    """
    
    result1 = execute_query(query1)
    if result1:
        print("✓ All customers (Relay connection):")
        print(json.dumps(result1, indent=2))
    
    # Test 2: All products with Relay connection
    query2 = """
    query {
        allProducts {
            edges {
                node {
                    id
                    name
                    price
                    stock
                }
            }
            pageInfo {
                hasNextPage
                hasPreviousPage
                startCursor
                endCursor
            }
        }
    }
    """
    
    result2 = execute_query(query2)
    if result2:
        print("\n✓ All products (Relay connection):")
        print(json.dumps(result2, indent=2))

def test_mutations():
    """Test mutations to create test data"""
    print("\n=== Testing Mutations ===")
    
    # Test 1: Create a customer
    mutation1 = """
    mutation {
        createCustomer(input: {
            name: "Test Customer"
            email: "test@example.com"
            phone: "+1234567890"
        }) {
            customer {
                id
                name
                email
                phone
            }
            success
            message
        }
    }
    """
    
    result1 = execute_query(mutation1)
    if result1:
        print("✓ Create customer:")
        print(json.dumps(result1, indent=2))
    
    # Test 2: Create a product
    mutation2 = """
    mutation {
        createProduct(input: {
            name: "Test Product"
            price: "99.99"
            stock: 50
        }) {
            product {
                id
                name
                price
                stock
            }
            success
            message
        }
    }
    """
    
    result2 = execute_query(mutation2)
    if result2:
        print("\n✓ Create product:")
        print(json.dumps(result2, indent=2))

if __name__ == "__main__":
    print("Starting GraphQL Filter Tests...")
    print("Make sure the Django server is running on http://127.0.0.1:8000")
    print("=" * 50)
    
    # Test mutations first to create some data
    test_mutations()
    
    # Test filtering functionality
    test_customer_filters()
    test_product_filters()
    test_order_filters()
    test_relay_connections()
    
    print("\n" + "=" * 50)
    print("Filter tests completed!") 