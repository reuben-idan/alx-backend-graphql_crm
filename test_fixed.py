import requests
import json

GRAPHQL_URL = "http://localhost:8000/graphql"

def test_query(query, variables=None):
    payload = {"query": query, "variables": variables or {}}
    response = requests.post(GRAPHQL_URL, json=payload)
    return response.json()

def test_hello():
    print("Testing hello query...")
    query = """
    query {
        hello
    }
    """
    result = test_query(query)
    print(json.dumps(result, indent=2))
    return result

def test_create_customer():
    print("\nTesting create customer mutation...")
    mutation = """
    mutation {
        createCustomer(input: {
            name: "Test Customer",
            email: "test@example.com",
            phone: "+1234567890"
        }) {
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
    result = test_query(mutation)
    print(json.dumps(result, indent=2))
    return result

def test_create_product():
    print("\nTesting create product mutation...")
    mutation = """
    mutation {
        createProduct(input: {
            name: "Test Product",
            price: "49.99",
            stock: 20
        }) {
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
    result = test_query(mutation)
    print(json.dumps(result, indent=2))
    return result

def test_create_order():
    print("\nTesting create order mutation...")
    # First get customer and product IDs
    query = """
    query {
        allCustomers {
            edges {
                node {
                    id
                }
            }
        }
        allProducts {
            edges {
                node {
                    id
                }
            }
        }
    }
    """
    data = test_query(query)
    
    if data.get('data'):
        customers = data['data']['allCustomers']['edges']
        products = data['data']['allProducts']['edges']
        
        if customers and products:
            customer_id = customers[0]['node']['id']
            product_ids = [products[0]['node']['id'], products[1]['node']['id']]
            
            mutation = f"""
            mutation {{
                createOrder(input: {{
                    customerId: "{customer_id}",
                    productIds: {json.dumps(product_ids)}
                }}) {{
                    order {{
                        id
                        customer {{
                            name
                        }}
                        totalAmount
                        orderDate
                    }}
                    message
                    success
                }}
            }}
            """
            result = test_query(mutation)
            print(json.dumps(result, indent=2))
            return result

def test_queries():
    print("\nTesting queries...")
    
    # Test all customers
    query = """
    query {
        allCustomers {
            edges {
                node {
                    id
                    name
                    email
                    phone
                }
            }
        }
    }
    """
    result = test_query(query)
    print("All customers:")
    print(json.dumps(result, indent=2))
    
    # Test all products
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
    print("\nAll products:")
    print(json.dumps(result, indent=2))
    
    # Test all orders (simplified)
    query = """
    query {
        allOrders {
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
    result = test_query(query)
    print("\nAll orders:")
    print(json.dumps(result, indent=2))

def test_filtering():
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
    print("Filter customers by name:")
    print(json.dumps(result, indent=2))
    
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
    print("\nFilter products by price range:")
    print(json.dumps(result, indent=2))

def main():
    print("Testing GraphQL CRM System (Fixed Version)...")
    
    try:
        # Test basic query
        test_hello()
        
        # Test queries
        test_queries()
        
        # Test mutations
        test_create_customer()
        test_create_product()
        test_create_order()
        
        # Test filtering
        test_filtering()
        
        print("\nAll tests completed!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 