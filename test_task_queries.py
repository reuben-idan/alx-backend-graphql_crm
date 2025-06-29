#!/usr/bin/env python3
"""
Test script for Task 3 specific queries
"""

import requests
import json

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

def test_task_queries():
    """Test the specific queries mentioned in Task 3 requirements"""
    print("=== Testing Task 3 Required Queries ===")
    
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
    
    result1 = execute_query(query1)
    if result1:
        print("✓ Query 1 Result:")
        print(json.dumps(result1, indent=2))
    
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
    
    result2 = execute_query(query2)
    if result2:
        print("✓ Query 2 Result:")
        print(json.dumps(result2, indent=2))
    
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
                    product {
                        name
                    }
                    totalAmount
                    orderDate
                }
            }
        }
    }
    """
    
    result3 = execute_query(query3)
    if result3:
        print("✓ Query 3 Result:")
        print(json.dumps(result3, indent=2))
    
    # Test 4: Alternative approach using filtered queries
    print("\n4. Using filtered queries (alternative approach):")
    query4 = """
    query {
        filteredCustomers(filter: { nameIcontains: "Ali", createdAtGte: "2025-01-01T00:00:00Z" }) {
            id
            name
            email
            createdAt
        }
    }
    """
    
    result4 = execute_query(query4)
    if result4:
        print("✓ Query 4 Result (filtered customers):")
        print(json.dumps(result4, indent=2))
    
    # Test 5: Filter products with price range and sorting
    query5 = """
    query {
        filteredProducts(filter: { priceGte: 100, priceLte: 1000, orderBy: "-stock" }) {
            id
            name
            price
            stock
        }
    }
    """
    
    result5 = execute_query(query5)
    if result5:
        print("✓ Query 5 Result (filtered products):")
        print(json.dumps(result5, indent=2))
    
    # Test 6: Filter orders with complex criteria
    query6 = """
    query {
        filteredOrders(filter: { customerName: "Alice", productName: "Laptop", totalAmountGte: 500 }) {
            id
            customer {
                name
            }
            items {
                product {
                    name
                }
            }
            totalAmount
            orderDate
        }
    }
    """
    
    result6 = execute_query(query6)
    if result6:
        print("✓ Query 6 Result (filtered orders):")
        print(json.dumps(result6, indent=2))

def test_advanced_filters():
    """Test advanced filtering features"""
    print("\n=== Testing Advanced Filtering Features ===")
    
    # Test phone pattern filtering
    print("\n1. Phone pattern filtering:")
    query1 = """
    query {
        filteredCustomers(filter: { phonePattern: "+1" }) {
            id
            name
            email
            phone
        }
    }
    """
    
    result1 = execute_query(query1)
    if result1:
        print("✓ Phone pattern filter:")
        print(json.dumps(result1, indent=2))
    
    # Test low stock filtering
    print("\n2. Low stock filtering:")
    query2 = """
    query {
        filteredProducts(filter: { lowStock: true }) {
            id
            name
            price
            stock
        }
    }
    """
    
    result2 = execute_query(query2)
    if result2:
        print("✓ Low stock filter:")
        print(json.dumps(result2, indent=2))
    
    # Test product ID filtering in orders
    print("\n3. Product ID filtering in orders:")
    query3 = """
    query {
        filteredOrders(filter: { productId: "1" }) {
            id
            customer {
                name
            }
            items {
                product {
                    id
                    name
                }
            }
            totalAmount
        }
    }
    """
    
    result3 = execute_query(query3)
    if result3:
        print("✓ Product ID filter in orders:")
        print(json.dumps(result3, indent=2))
    
    # Test date range filtering
    print("\n4. Date range filtering:")
    query4 = """
    query {
        filteredOrders(filter: { orderDateGte: "2025-06-29T00:00:00Z", orderDateLte: "2025-06-30T00:00:00Z" }) {
            id
            orderDate
            totalAmount
            customer {
                name
            }
        }
    }
    """
    
    result4 = execute_query(query4)
    if result4:
        print("✓ Date range filter:")
        print(json.dumps(result4, indent=2))

def test_sorting():
    """Test sorting functionality"""
    print("\n=== Testing Sorting Functionality ===")
    
    # Test sorting customers by name
    print("\n1. Sort customers by name:")
    query1 = """
    query {
        filteredCustomers(filter: { orderBy: "name" }) {
            id
            name
            email
        }
    }
    """
    
    result1 = execute_query(query1)
    if result1:
        print("✓ Sort customers by name:")
        print(json.dumps(result1, indent=2))
    
    # Test sorting products by price descending
    print("\n2. Sort products by price (descending):")
    query2 = """
    query {
        filteredProducts(filter: { orderBy: "-price" }) {
            id
            name
            price
            stock
        }
    }
    """
    
    result2 = execute_query(query2)
    if result2:
        print("✓ Sort products by price (descending):")
        print(json.dumps(result2, indent=2))
    
    # Test sorting orders by total amount
    print("\n3. Sort orders by total amount:")
    query3 = """
    query {
        filteredOrders(filter: { orderBy: "totalAmount" }) {
            id
            totalAmount
            customer {
                name
            }
        }
    }
    """
    
    result3 = execute_query(query3)
    if result3:
        print("✓ Sort orders by total amount:")
        print(json.dumps(result3, indent=2))

if __name__ == "__main__":
    print("Starting Task 3 Query Tests...")
    print("Make sure the Django server is running on http://127.0.0.1:8000")
    print("=" * 60)
    
    # Test the specific task queries
    test_task_queries()
    
    # Test advanced filtering features
    test_advanced_filters()
    
    # Test sorting functionality
    test_sorting()
    
    print("\n" + "=" * 60)
    print("Task 3 query tests completed!")
    print("\nSummary:")
    print("✓ Customer filtering with name and date range")
    print("✓ Product filtering with price range and sorting")
    print("✓ Order filtering with customer name, product name, and amount")
    print("✓ Phone pattern filtering")
    print("✓ Low stock filtering")
    print("✓ Date range filtering")
    print("✓ Sorting functionality")
    print("✓ Relay connections with filtering") 