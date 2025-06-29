import requests
import json

GRAPHQL_URL = "http://localhost:8000/graphql"

def test_query(query, variables=None):
    payload = {"query": query, "variables": variables or {}}
    response = requests.post(GRAPHQL_URL, json=payload)
    return response.json()

def test_create_customer():
    print("Testing create customer mutation...")
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

def test_bulk_create_customers():
    print("\nTesting bulk create customers mutation...")
    mutation = """
    mutation {
        bulkCreateCustomers(input: [
            { name: "Bulk Customer 1", email: "bulk1@example.com", phone: "123-456-7890" },
            { name: "Bulk Customer 2", email: "bulk2@example.com" }
        ]) {
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
    result = test_query(mutation)
    print(json.dumps(result, indent=2))
    return result

def test_create_product():
    print("\nTesting create product mutation...")
    mutation = """
    mutation {
        createProduct(input: {
            name: "Test Product",
            price: 49.99,
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
                        products {{
                            name
                            price
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
    
    # Test all orders
    query = """
    query {
        allOrders {
            edges {
                node {
                    id
                    customer {
                        name
                    }
                    products {
                        name
                        price
                    }
                    totalAmount
                }
            }
        }
    }
    """
    result = test_query(query)
    print("\nAll orders:")
    print(json.dumps(result, indent=2))

def main():
    print("Testing GraphQL CRM System...")
    
    try:
        # Test queries first
        test_queries()
        
        # Test mutations
        test_create_customer()
        test_bulk_create_customers()
        test_create_product()
        test_create_order()
        
        print("\nAll tests completed!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 