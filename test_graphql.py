#!/usr/bin/env python
import requests
import json

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

def test_query(query, variables=None):
    """Test a GraphQL query"""
    payload = {
        "query": query,
        "variables": variables or {}
    }
    
    response = requests.post(GRAPHQL_URL, json=payload)
    return response.json()

def test_mutation(mutation, variables=None):
    """Test a GraphQL mutation"""
    payload = {
        "query": mutation,
        "variables": variables or {}
    }
    
    response = requests.post(GRAPHQL_URL, json=payload)
    return response.json()

def test_hello_query():
    """Test the hello query"""
    print("Testing hello query...")
    query = """
    query {
        hello
    }
    """
    result = test_query(query)
    print(f"Result: {result}")
    return result

def test_customer_queries():
    """Test customer queries"""
    print("\nTesting customer queries...")
    
    # Get all customers
    query = """
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
        }
    }
    """
    result = test_query(query)
    print(f"All customers: {result}")
    
    # Get specific customer
    if result.get('data', {}).get('allCustomers', {}).get('edges'):
        customer_id = result['data']['allCustomers']['edges'][0]['node']['id']
        query = f"""
        query {{
            customer(id: "{customer_id}") {{
                id
                name
                email
                phone
            }}
        }}
        """
        result = test_query(query)
        print(f"Specific customer: {result}")

def test_product_queries():
    """Test product queries"""
    print("\nTesting product queries...")
    
    query = """
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
        }
    }
    """
    result = test_query(query)
    print(f"All products: {result}")

def test_order_queries():
    """Test order queries"""
    print("\nTesting order queries...")
    
    query = """
    query {
        allOrders {
            edges {
                node {
                    id
                    customer {
                        name
                        email
                    }
                    products {
                        name
                        price
                    }
                    totalAmount
                    orderDate
                }
            }
        }
    }
    """
    result = test_query(query)
    print(f"All orders: {result}")

def test_create_customer_mutation():
    """Test create customer mutation"""
    print("\nTesting create customer mutation...")
    
    mutation = """
    mutation CreateCustomer($input: CreateCustomerInput!) {
        createCustomer(input: $input) {
            customer {
                id
                name
                email
                phone
            }
            message
            success
        }
    }
    """
    
    variables = {
        "input": {
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "+1234567890"
        }
    }
    
    result = test_mutation(mutation, variables)
    print(f"Create customer result: {result}")
    return result

def test_bulk_create_customers_mutation():
    """Test bulk create customers mutation"""
    print("\nTesting bulk create customers mutation...")
    
    mutation = """
    mutation BulkCreateCustomers($input: [CreateCustomerInput!]!) {
        bulkCreateCustomers(input: $input) {
            customers {
                id
                name
                email
            }
            errors
            success
        }
    }
    """
    
    variables = {
        "input": [
            {
                "name": "Bulk Customer 1",
                "email": "bulk1@example.com",
                "phone": "123-456-7890"
            },
            {
                "name": "Bulk Customer 2",
                "email": "bulk2@example.com"
            }
        ]
    }
    
    result = test_mutation(mutation, variables)
    print(f"Bulk create customers result: {result}")

def test_create_product_mutation():
    """Test create product mutation"""
    print("\nTesting create product mutation...")
    
    mutation = """
    mutation CreateProduct($input: CreateProductInput!) {
        createProduct(input: $input) {
            product {
                id
                name
                price
                stock
            }
            message
            success
        }
    }
    """
    
    variables = {
        "input": {
            "name": "Test Product",
            "price": "49.99",
            "stock": 20
        }
    }
    
    result = test_mutation(mutation, variables)
    print(f"Create product result: {result}")
    return result

def test_create_order_mutation():
    """Test create order mutation"""
    print("\nTesting create order mutation...")
    
    # First get a customer and products
    customer_query = """
    query {
        allCustomers {
            edges {
                node {
                    id
                }
            }
        }
    }
    """
    
    product_query = """
    query {
        allProducts {
            edges {
                node {
                    id
                }
            }
        }
    }
    """
    
    customer_result = test_query(customer_query)
    product_result = test_query(product_query)
    
    if (customer_result.get('data', {}).get('allCustomers', {}).get('edges') and 
        product_result.get('data', {}).get('allProducts', {}).get('edges')):
        
        customer_id = customer_result['data']['allCustomers']['edges'][0]['node']['id']
        product_ids = [edge['node']['id'] for edge in product_result['data']['allProducts']['edges'][:2]]
        
        mutation = """
        mutation CreateOrder($input: CreateOrderInput!) {
            createOrder(input: $input) {
                order {
                    id
                    customer {
                        name
                    }
                    products {
                        name
                        price
                    }
                    totalAmount
                    orderDate
                }
                message
                success
            }
        }
        """
        
        variables = {
            "input": {
                "customerId": customer_id,
                "productIds": product_ids
            }
        }
        
        result = test_mutation(mutation, variables)
        print(f"Create order result: {result}")

def test_filtering():
    """Test filtering functionality"""
    print("\nTesting filtering...")
    
    # Filter customers by name
    query = """
    query {
        allCustomers(filter: {nameIcontains: "Alice"}) {
            edges {
                node {
                    id
                    name
                    email
                }
            }
        }
    }
    """
    result = test_query(query)
    print(f"Filter customers by name: {result}")
    
    # Filter products by price range
    query = """
    query {
        allProducts(filter: {priceGte: 100, priceLte: 1000}) {
            edges {
                node {
                    id
                    name
                    price
                }
            }
        }
    }
    """
    result = test_query(query)
    print(f"Filter products by price range: {result}")

def main():
    """Run all tests"""
    print("Starting GraphQL tests...")
    
    try:
        # Test basic query
        test_hello_query()
        
        # Test queries
        test_customer_queries()
        test_product_queries()
        test_order_queries()
        
        # Test mutations
        test_create_customer_mutation()
        test_bulk_create_customers_mutation()
        test_create_product_mutation()
        test_create_order_mutation()
        
        # Test filtering
        test_filtering()
        
        print("\nAll tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to GraphQL server. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main() 