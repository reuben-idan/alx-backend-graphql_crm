import os
import sys
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """
    Log a heartbeat message to confirm CRM application health.
    Optionally queries the GraphQL hello field to verify endpoint responsiveness.
    """
    # Get current timestamp in DD/MM/YYYY-HH:MM:SS format
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    
    # Create the heartbeat message
    heartbeat_message = f"{timestamp} CRM is alive\n"
    
    # Log to the specified file (append mode)
    try:
        log_file = 'C:/temp/crm_heartbeat_log.txt' if os.name == 'nt' else '/tmp/crm_heartbeat_log.txt'
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(heartbeat_message)
    except Exception as e:
        print(f"Error writing to heartbeat log: {e}")
    
    # Optionally query the GraphQL hello field to verify endpoint responsiveness
    try:
        # Setup Django environment if needed
        if 'DJANGO_SETTINGS_MODULE' not in os.environ:
            # Add the project directory to Python path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_dir = os.path.dirname(script_dir)
            sys.path.insert(0, project_dir)
            
            # Set Django settings
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
            
            # Import Django after setting up the environment
            import django
            django.setup()
        
        # GraphQL endpoint
        GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"
        
        # GraphQL query to test hello field
        HELLO_QUERY = gql("""
            query {
                hello
            }
        """)
        
        # Create GraphQL client and execute query
        transport = RequestsHTTPTransport(url=GRAPHQL_ENDPOINT)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        result = client.execute(HELLO_QUERY)
        
        # Log successful GraphQL query
        graphql_status = f"{timestamp} GraphQL endpoint responsive: {result.get('hello', 'Unknown response')}\n"
        log_file = 'C:/temp/crm_heartbeat_log.txt' if os.name == 'nt' else '/tmp/crm_heartbeat_log.txt'
        with open(log_file, 'a') as f:
            f.write(graphql_status)
            
    except Exception as e:
        # Log GraphQL query failure
        graphql_error = f"{timestamp} GraphQL endpoint check failed: {str(e)}\n"
        log_file = 'C:/temp/crm_heartbeat_log.txt' if os.name == 'nt' else '/tmp/crm_heartbeat_log.txt'
        with open(log_file, 'a') as f:
            f.write(graphql_error)


def update_low_stock():
    """
    Execute the UpdateLowStockProducts mutation via GraphQL endpoint.
    Log updated product names and new stock levels.
    """
    # Get current timestamp
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    
    try:
        # Setup Django environment if needed
        if 'DJANGO_SETTINGS_MODULE' not in os.environ:
            # Add the project directory to Python path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_dir = os.path.dirname(script_dir)
            sys.path.insert(0, project_dir)
            
            # Set Django settings
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
            
            # Import Django after setting up the environment
            import django
            django.setup()
        
        # GraphQL endpoint
        GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"
        
        # GraphQL mutation to update low stock products
        UPDATE_LOW_STOCK_MUTATION = gql("""
            mutation {
                updateLowStockProducts {
                    success
                    message
                    updatedProducts {
                        id
                        name
                        stock
                        price
                    }
                }
            }
        """)
        
        # Create GraphQL client and execute mutation
        transport = RequestsHTTPTransport(url=GRAPHQL_ENDPOINT)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        result = client.execute(UPDATE_LOW_STOCK_MUTATION)
        
        # Extract results
        mutation_result = result.get('updateLowStockProducts', {})
        success = mutation_result.get('success', False)
        message = mutation_result.get('message', 'Unknown response')
        updated_products = mutation_result.get('updatedProducts', [])
        
        # Log the results
        log_file = 'C:/temp/low_stock_updates_log.txt' if os.name == 'nt' else '/tmp/low_stock_updates_log.txt'
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(f"\n{timestamp}: Low stock update process started\n")
            f.write(f"{timestamp}: Success: {success}\n")
            f.write(f"{timestamp}: Message: {message}\n")
            
            if updated_products:
                f.write(f"{timestamp}: Updated products:\n")
                for product in updated_products:
                    product_name = product.get('name', 'Unknown')
                    new_stock = product.get('stock', 0)
                    product_id = product.get('id', 'Unknown')
                    f.write(f"{timestamp}: - Product: {product_name} (ID: {product_id}) - New Stock: {new_stock}\n")
            else:
                f.write(f"{timestamp}: No products were updated\n")
                
    except Exception as e:
        # Log error
        log_file = 'C:/temp/low_stock_updates_log.txt' if os.name == 'nt' else '/tmp/low_stock_updates_log.txt'
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        error_message = f"{timestamp}: Error updating low stock products: {str(e)}\n"
        with open(log_file, 'a') as f:
            f.write(error_message) 