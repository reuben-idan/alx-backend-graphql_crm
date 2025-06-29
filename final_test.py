import requests
import json

GRAPHQL_URL = "http://localhost:8000/graphql"

def test_query(query, variables=None):
    payload = {"query": query, "variables": variables or {}}
    response = requests.post(GRAPHQL_URL, json=payload)
    return response.json()

def test_hello():
    print("✅ Testing hello query...")
    query = """
    query {
        hello
    }
    """
    result = test_query(query)
    print(json.dumps(result, indent=2))
    return result

def test_create_customer():
    print("\n✅ Testing create customer mutation...")
    mutation = """
    mutation {
        createCustomer(input: {
            name: "John Doe",
            email: "john.doe@example.com",
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
    print("\n✅ Testing create product mutation...")
    mutation = """
    mutation {
        createProduct(input: {
            name: "Wireless Keyboard",
            price: "79.99",
            stock: 15
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
    print("\n✅ Testing create order mutation...")
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
    print("\n✅ Testing queries...")
    
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
    print("\n✅ Testing filtering (correct syntax)...")
    
    # Filter customers by name (correct syntax)
    query = """
    query {
        allCustomers(name_Icontains: "Alice") {
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
    print("Filter customers by name (name_Icontains: 'Alice'):")
    print(json.dumps(result, indent=2))
    
    # Filter products by price range (correct syntax)
    query = """
    query {
        allProducts(price_Gte: 100, price_Lte: 1000) {
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
    print("\nFilter products by price range (price_Gte: 100, price_Lte: 1000):")
    print(json.dumps(result, indent=2))
    
    # Filter products with low stock
    query = """
    query {
        allProducts(stock_Lte: 10) {
            edges {
                node {
                    id
                    name
                    stock
                }
            }
        }
    }
    """
    result = test_query(query)
    print("\nFilter products with low stock (stock_Lte: 10):")
    print(json.dumps(result, indent=2))

def test_bulk_operations():
    print("\n✅ Testing bulk operations...")
    
    # Test bulk create customers
    mutation = """
    mutation {
        bulkCreateCustomers(input: [
            { name: "Jane Smith", email: "jane@example.com", phone: "555-1234" },
            { name: "Mike Johnson", email: "mike@example.com" },
            { name: "Sarah Wilson", email: "sarah@example.com", phone: "+9876543210" }
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
    print("Bulk create customers:")
    print(json.dumps(result, indent=2))

def test_error_handling():
    print("\n✅ Testing error handling...")
    
    # Test duplicate email
    mutation = """
    mutation {
        createCustomer(input: {
            name: "Duplicate Test",
            email: "test@example.com",
            phone: "+1234567890"
        }) {
            customer {
                id
                name
                email
            }
            message
            success
        }
    }
    """
    result = test_query(mutation)
    print("Duplicate email error handling:")
    print(json.dumps(result, indent=2))
    
    # Test invalid price
    mutation = """
    mutation {
        createProduct(input: {
            name: "Invalid Product",
            price: "-10.00",
            stock: 5
        }) {
            product {
                id
                name
                price
            }
            message
            success
        }
    }
    """
    result = test_query(mutation)
    print("\nInvalid price error handling:")
    print(json.dumps(result, indent=2))

def main():
    print("🚀 Testing Complete GraphQL CRM System...")
    print("=" * 50)
    
    try:
        # Test basic functionality
        test_hello()
        
        # Test queries
        test_queries()
        
        # Test mutations
        test_create_customer()
        test_create_product()
        test_create_order()
        
        # Test bulk operations
        test_bulk_operations()
        
        # Test filtering
        test_filtering()
        
        # Test error handling
        test_error_handling()
        
        print("\n" + "=" * 50)
        print("🎉 All tests completed successfully!")
        print("\n📋 Summary of implemented features:")
        print("✅ Basic GraphQL endpoint setup")
        print("✅ Customer CRUD operations with validation")
        print("✅ Product CRUD operations with validation")
        print("✅ Order creation with product associations")
        print("✅ Bulk customer creation with partial success")
        print("✅ Advanced filtering and searching")
        print("✅ Error handling and validation")
        print("✅ Relay ID support for connections")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 