#!/bin/bash

# Customer Cleanup Script
# Deletes customers with no orders since a year ago

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Store current working directory (cwd)
cwd=$(pwd)

# Change to the project directory
cd "$PROJECT_DIR"

# Check if we successfully changed to the project directory
if [ "$(pwd)" = "$PROJECT_DIR" ]; then
    echo "Successfully changed to project directory: $(pwd)"
else
    echo "Failed to change to project directory. Current directory: $(pwd)"
    exit 1
fi

# Execute the cleanup command using Django shell
python manage.py shell << EOF
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

# Calculate the date one year ago
one_year_ago = timezone.now() - timedelta(days=365)

# Find customers with no orders since a year ago
customers_to_delete = []
for customer in Customer.objects.all():
    # Check if customer has any orders since one year ago
    recent_orders = customer.orders.filter(order_date__gte=one_year_ago)
    if not recent_orders.exists():
        customers_to_delete.append(customer)
    else:
        # Customer has recent orders, keep them
        pass

# Delete the customers
deleted_count = len(customers_to_delete)
for customer in customers_to_delete:
    customer.delete()

print(f"Deleted {deleted_count} inactive customers")
EOF

# Log the results with timestamp
echo "$(date): Customer cleanup completed. Deleted $(python manage.py shell -c "from django.utils import timezone; from datetime import timedelta; from crm.models import Customer; one_year_ago = timezone.now() - timedelta(days=365); customers_to_delete = [c for c in Customer.objects.all() if not c.orders.filter(order_date__gte=one_year_ago).exists()]; print(len(customers_to_delete))") inactive customers." >> /tmp/customer_cleanup_log.txt

# Return to original directory
cd "$cwd" 