#!/usr/bin/env python3

import os
import sys
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

# GraphQL query to get orders from the last 7 days
QUERY = gql("""
    query GetRecentOrders($startDate: DateTime!) {
        orders(orderDate_Gte: $startDate) {
            id
            orderDate
            customer {
                email
                name
            }
        }
    }
""")

def setup_django_environment():
    """Setup Django environment for the script."""
    # Add the project directory to Python path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    sys.path.insert(0, project_dir)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
    
    # Import Django after setting up the environment
    import django
    django.setup()

def get_recent_orders():
    """Query GraphQL for orders from the last 7 days."""
    try:
        # Create GraphQL client
        transport = RequestsHTTPTransport(url=GRAPHQL_ENDPOINT)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # Calculate date 7 days ago
        start_date = (datetime.now() - timedelta(days=7)).isoformat()
        
        # Execute the query
        result = client.execute(QUERY, variable_values={'startDate': start_date})
        
        return result.get('orders', [])
    except Exception as e:
        print(f"Error querying GraphQL: {e}")
        return []

def log_order_reminders(orders):
    """Log order reminders to file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open('/tmp/order_reminders_log.txt', 'a') as f:
        f.write(f"\n{timestamp}: Processing order reminders\n")
        
        if not orders:
            f.write(f"{timestamp}: No recent orders found\n")
            return
        
        for order in orders:
            order_id = order.get('id', 'Unknown')
            customer_email = order.get('customer', {}).get('email', 'Unknown')
            customer_name = order.get('customer', {}).get('name', 'Unknown')
            order_date = order.get('orderDate', 'Unknown')
            
            log_entry = f"{timestamp}: Order ID {order_id} - Customer: {customer_name} ({customer_email}) - Date: {order_date}\n"
            f.write(log_entry)

def main():
    """Main function to process order reminders."""
    # Setup Django environment
    setup_django_environment()
    
    # Get recent orders from GraphQL
    orders = get_recent_orders()
    
    # Log the reminders
    log_order_reminders(orders)
    
    # Print completion message
    print("Order reminders processed!")

if __name__ == "__main__":
    main() 