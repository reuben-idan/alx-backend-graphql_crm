#!/usr/bin/env python
"""
Database seeding script for the GraphQL CRM system.
This script creates sample customers, products, and orders for testing.
"""

import os
import django
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
django.setup()

from crm.models import Customer, Product, Order, OrderItem

# Clear existing data
OrderItem.objects.all().delete()
Order.objects.all().delete()
Product.objects.all().delete()
Customer.objects.all().delete()

# Create sample customers
customer1 = Customer.objects.create(
    name="John Doe",
    email="john@example.com",
    phone="+1234567890"
)

customer2 = Customer.objects.create(
    name="Jane Smith",
    email="jane@example.com",
    phone="123-456-7890"
)

customer3 = Customer.objects.create(
    name="Bob Johnson",
    email="bob@example.com"
)

# Create sample products
product1 = Product.objects.create(
    name="Laptop Pro",
    price=Decimal("1299.99"),
    stock=25
)

product2 = Product.objects.create(
    name="Wireless Mouse",
    price=Decimal("49.99"),
    stock=100
)

product3 = Product.objects.create(
    name="Mechanical Keyboard",
    price=Decimal("149.99"),
    stock=50
)

# Create sample orders
order1 = Order.objects.create(
    customer=customer1,
    total_amount=Decimal("1349.98")
)

order2 = Order.objects.create(
    customer=customer2,
    total_amount=Decimal("149.99")
)

# Create order items
OrderItem.objects.create(
    order=order1,
    product=product1,
    quantity=1,
    unit_price=product1.price
)

OrderItem.objects.create(
    order=order1,
    product=product2,
    quantity=1,
    unit_price=product2.price
)

OrderItem.objects.create(
    order=order2,
    product=product3,
    quantity=1,
    unit_price=product3.price
)

print("✅ Sample data created successfully!")
print(f"Customers: {Customer.objects.count()}")
print(f"Products: {Product.objects.count()}")
print(f"Orders: {Order.objects.count()}")
print(f"Order Items: {OrderItem.objects.count()}")

print("\n🚀 You can now:")
print("   1. Start the server: python manage.py runserver")
print("   2. Visit GraphiQL: http://127.0.0.1:8000/graphql")
print("   3. Visit Admin: http://127.0.0.1:8000/admin")
print("   4. Try the sample queries from the README")

if __name__ == "__main__":
    pass 