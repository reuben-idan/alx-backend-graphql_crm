import os
import sys
from datetime import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    """
    Generate a weekly CRM report using GraphQL queries.
    Fetches total customers, orders, and revenue.
    """
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
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
        
        # GraphQL query to get CRM statistics
        CRM_STATS_QUERY = gql("""
            query {
                customers {
                    id
                }
                orders {
                    id
                    totalAmount
                }
            }
        """)
        
        # Create GraphQL client and execute query
        transport = RequestsHTTPTransport(url=GRAPHQL_ENDPOINT)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        result = client.execute(CRM_STATS_QUERY)
        
        # Extract data
        customers = result.get('customers', [])
        orders = result.get('orders', [])
        
        # Calculate statistics
        total_customers = len(customers)
        total_orders = len(orders)
        total_revenue = sum(float(order.get('totalAmount', 0)) for order in orders)
        
        # Format the report
        report_message = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, ${total_revenue:.2f} revenue"
        
        # Log the report
        log_file = 'C:/temp/crm_report_log.txt' if os.name == 'nt' else '/tmp/crm_report_log.txt'
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(f"{report_message}\n")
        
        return {
            'success': True,
            'customers': total_customers,
            'orders': total_orders,
            'revenue': total_revenue,
            'message': report_message
        }
        
    except Exception as e:
        # Log error
        error_message = f"{timestamp} - Error generating CRM report: {str(e)}"
        log_file = 'C:/temp/crm_report_log.txt' if os.name == 'nt' else '/tmp/crm_report_log.txt'
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(f"{error_message}\n")
        
        return {
            'success': False,
            'error': str(e),
            'message': error_message
        } 