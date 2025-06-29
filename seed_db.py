#!/usr/bin/env python
import os
import django
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graphql_crm.settings')
django.setup()

from crm.models import Customer, Product, Order, OrderItem

def seed_database():
    print("Seeding database...")
    
    # Clear existing data
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    Product.objects.all().delete()
    Customer.objects.all().delete()
    
    # Create customers
    customers = [
        Customer.objects.create(
            name="Alice Johnson",
            email="alice@example.com",
            phone="+1234567890"
        ),
        Customer.objects.create(
            name="Bob Smith",
            email="bob@example.com",
            phone="123-456-7890"
        ),
        Customer.objects.create(
            name="Carol Davis",
            email="carol@example.com",
            phone="+1987654321"
        ),
        Customer.objects.create(
            name="David Wilson",
            email="david@example.com"
        ),
    ]
    
    # Create products
    products = [
        Product.objects.create(
            name="Laptop",
            price=Decimal('999.99'),
            stock=10
        ),
        Product.objects.create(
            name="Smartphone",
            price=Decimal('599.99'),
            stock=25
        ),
        Product.objects.create(
            name="Headphones",
            price=Decimal('99.99'),
            stock=50
        ),
        Product.objects.create(
            name="Tablet",
            price=Decimal('399.99'),
            stock=5
        ),
        Product.objects.create(
            name="Mouse",
            price=Decimal('29.99'),
            stock=100
        ),
    ]
    
    # Create orders
    orders = [
        Order.objects.create(
            customer=customers[0],
            total_amount=Decimal('1099.98')
        ),
        Order.objects.create(
            customer=customers[1],
            total_amount=Decimal('699.98')
        ),
        Order.objects.create(
            customer=customers[2],
            total_amount=Decimal('129.98')
        ),
    ]
    
    # Create order items
    OrderItem.objects.create(
        order=orders[0],
        product=products[0],  # Laptop
        quantity=1,
        price=Decimal('999.99')
    )
    OrderItem.objects.create(
        order=orders[0],
        product=products[2],  # Headphones
        quantity=1,
        price=Decimal('99.99')
    )
    
    OrderItem.objects.create(
        order=orders[1],
        product=products[1],  # Smartphone
        quantity=1,
        price=Decimal('599.99')
    )
    OrderItem.objects.create(
        order=orders[1],
        product=products[4],  # Mouse
        quantity=1,
        price=Decimal('29.99')
    )
    
    OrderItem.objects.create(
        order=orders[2],
        product=products[2],  # Headphones
        quantity=1,
        price=Decimal('99.99')
    )
    OrderItem.objects.create(
        order=orders[2],
        product=products[4],  # Mouse
        quantity=1,
        price=Decimal('29.99')
    )
    
    # Associate products with orders
    orders[0].products.add(products[0], products[2])
    orders[1].products.add(products[1], products[4])
    orders[2].products.add(products[2], products[4])
    
    print(f"Created {len(customers)} customers")
    print(f"Created {len(products)} products")
    print(f"Created {len(orders)} orders")
    print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database() 