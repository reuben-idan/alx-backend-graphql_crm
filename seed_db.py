# seed_db.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

from crm.models import Customer, Product, Order
from django.utils import timezone
from decimal import Decimal

# Clear existing data
Order.objects.all().delete()
Customer.objects.all().delete()
Product.objects.all().delete()

# Create customers
customers = [
    Customer(name="Alice", email="alice@example.com", phone="+1234567890"),
    Customer(name="Bob", email="bob@example.com", phone="123-456-7890"),
    Customer(name="Carol", email="carol@example.com")
]
Customer.objects.bulk_create(customers)

# Create products
products = [
    Product(name="Laptop", price=Decimal('999.99'), stock=10),
    Product(name="Smartphone", price=Decimal('499.99'), stock=20),
    Product(name="Headphones", price=Decimal('149.99'), stock=50)
]
Product.objects.bulk_create(products)

# Create a sample order
order = Order.objects.create(
    customer=Customer.objects.get(email="alice@example.com"),
    total_amount=Decimal('1149.98'),
    order_date=timezone.now()
)
order.products.set(Product.objects.filter(name__in=["Laptop", "Headphones"]))

print("✅ Database seeded successfully.")
