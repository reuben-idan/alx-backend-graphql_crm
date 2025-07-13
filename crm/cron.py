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
        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
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
        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
            f.write(graphql_status)
            
    except Exception as e:
        # Log GraphQL query failure
        graphql_error = f"{timestamp} GraphQL endpoint check failed: {str(e)}\n"
        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
            f.write(graphql_error) 