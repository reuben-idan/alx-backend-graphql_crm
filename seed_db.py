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
from django.utils import timezone
from datetime import timedelta


def create_sample_data():
    """Create sample data for the CRM system."""
    
    print("🌱 Seeding database with sample data...")
    
    # Clear existing data
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    Product.objects.all().delete()
    Customer.objects.all().delete()
    
    print("🗑️  Cleared existing data")
    
    # Create customers
    customers = [
        Customer.objects.create(
            name="John Doe",
            email="john@example.com",
            phone="+1234567890",
            address="123 Main St, NY"
        ),
        Customer.objects.create(
            name="Jane Smith",
            email="jane@example.com",
            phone="+1987654321",
            address="456 Oak Ave, CA"
        ),
        Customer.objects.create(
            name="Bob Johnson",
            email="bob.johnson@example.com",
            phone="+1555123456",
            address="789 Pine Rd, Chicago, IL 60601"
        ),
        Customer.objects.create(
            name="Alice Brown",
            email="alice.brown@example.com",
            phone="+1777888999",
            address="321 Elm St, Miami, FL 33101"
        ),
        Customer.objects.create(
            name="Charlie Wilson",
            email="charlie.wilson@example.com",
            phone="+1444333222",
            address="654 Maple Dr, Seattle, WA 98101"
        )
    ]
    
    print(f"👥 Created {len(customers)} customers")
    
    # Create products
    products = [
        Product.objects.create(
            name="Laptop Pro",
            description="High-performance laptop",
            price=Decimal("1299.99"),
            stock_quantity=25,
            sku="LAP-001"
        ),
        Product.objects.create(
            name="Wireless Mouse",
            description="Ergonomic wireless mouse",
            price=Decimal("49.99"),
            stock_quantity=100,
            sku="MOU-002"
        ),
        Product.objects.create(
            name="Mechanical Keyboard",
            description="RGB mechanical keyboard with Cherry MX switches",
            price=Decimal("149.99"),
            stock_quantity=50,
            sku="KEY-MK-003"
        ),
        Product.objects.create(
            name="4K Monitor",
            description="27-inch 4K Ultra HD monitor with HDR support",
            price=Decimal("399.99"),
            stock_quantity=30,
            sku="MON-4K-004"
        ),
        Product.objects.create(
            name="USB-C Hub",
            description="7-port USB-C hub with HDMI and Ethernet",
            price=Decimal("79.99"),
            stock_quantity=75,
            sku="HUB-UC-005"
        ),
        Product.objects.create(
            name="Gaming Headset",
            description="7.1 surround sound gaming headset with microphone",
            price=Decimal("89.99"),
            stock_quantity=60,
            sku="AUD-GH-006"
        ),
        Product.objects.create(
            name="External SSD",
            description="1TB external SSD with USB 3.1 Gen 2",
            price=Decimal("129.99"),
            stock_quantity=40,
            sku="SSD-EX-007"
        ),
        Product.objects.create(
            name="Webcam HD",
            description="1080p HD webcam with autofocus and noise cancellation",
            price=Decimal("69.99"),
            stock_quantity=80,
            sku="CAM-HD-008"
        )
    ]
    
    print(f"📦 Created {len(products)} products")
    
    # Create orders with different dates
    orders = []
    
    # Order 1 - John Doe
    order1 = Order.objects.create(
        customer=customers[0],
        status='delivered',
        order_date=timezone.now() - timedelta(days=30),
        shipping_address="123 Main St, NY",
        notes="Deliver during business hours"
    )
    orders.append(order1)
    
    # Order 2 - Jane Smith
    order2 = Order.objects.create(
        customer=customers[1],
        status='pending',
        order_date=timezone.now() - timedelta(days=15),
        shipping_address="456 Oak Ave, CA",
        notes=""
    )
    orders.append(order2)
    
    # Order 3 - Bob Johnson
    order3 = Order.objects.create(
        customer=customers[2],
        status='processing',
        order_date=timezone.now() - timedelta(days=7),
        shipping_address="789 Pine Rd, Chicago, IL 60601",
        notes=""
    )
    orders.append(order3)
    
    # Order 4 - Alice Brown
    order4 = Order.objects.create(
        customer=customers[3],
        status='pending',
        order_date=timezone.now() - timedelta(days=2),
        shipping_address="321 Elm St, Miami, FL 33101",
        notes="Rush order if possible"
    )
    orders.append(order4)
    
    # Order 5 - Charlie Wilson
    order5 = Order.objects.create(
        customer=customers[4],
        status='cancelled',
        order_date=timezone.now() - timedelta(days=45),
        shipping_address="654 Maple Dr, Seattle, WA 98101",
        notes="Cancelled due to change of mind"
    )
    orders.append(order5)
    
    # Order 6 - John Doe (second order)
    order6 = Order.objects.create(
        customer=customers[0],
        status='pending',
        order_date=timezone.now() - timedelta(days=1),
        shipping_address="123 Main St, NY",
        notes=""
    )
    orders.append(order6)
    
    print(f"📋 Created {len(orders)} orders")
    
    # Create order items
    order_items = []
    
    # Order 1 items
    OrderItem.objects.create(
        order=order1,
        product=products[0],  # Laptop
        quantity=1,
        unit_price=products[0].price
    )
    OrderItem.objects.create(
        order=order1,
        product=products[1],  # Mouse
        quantity=2,
        unit_price=products[1].price
    )
    
    # Order 2 items
    OrderItem.objects.create(
        order=order2,
        product=products[2],  # Keyboard
        quantity=1,
        unit_price=products[2].price
    )
    OrderItem.objects.create(
        order=order2,
        product=products[5],  # Headset
        quantity=1,
        unit_price=products[5].price
    )
    
    # Order 3 items
    OrderItem.objects.create(
        order=order3,
        product=products[3],  # Monitor
        quantity=2,
        unit_price=products[3].price
    )
    OrderItem.objects.create(
        order=order3,
        product=products[4],  # USB Hub
        quantity=1,
        unit_price=products[4].price
    )
    
    # Order 4 items
    OrderItem.objects.create(
        order=order4,
        product=products[6],  # External SSD
        quantity=1,
        unit_price=products[6].price
    )
    OrderItem.objects.create(
        order=order4,
        product=products[7],  # Webcam
        quantity=1,
        unit_price=products[7].price
    )
    
    # Order 5 items (cancelled)
    OrderItem.objects.create(
        order=order5,
        product=products[0],  # Laptop
        quantity=1,
        unit_price=products[0].price
    )
    
    # Order 6 items
    OrderItem.objects.create(
        order=order6,
        product=products[1],  # Mouse
        quantity=2,
        unit_price=products[1].price
    )
    OrderItem.objects.create(
        order=order6,
        product=products[4],  # USB Hub
        quantity=1,
        unit_price=products[4].price
    )
    
    total_items = OrderItem.objects.count()
    print(f"🛒 Created {total_items} order items")
    
    # Print summary
    print("\n📊 Database Summary:")
    print(f"   Customers: {Customer.objects.count()}")
    print(f"   Products: {Product.objects.count()}")
    print(f"   Orders: {Order.objects.count()}")
    print(f"   Order Items: {OrderItem.objects.count()}")
    
    # Print some sample data
    print("\n🎯 Sample Data Created:")
    print(f"   Customer: {customers[0].name} ({customers[0].email})")
    print(f"   Product: {products[0].name} - ${products[0].price}")
    print(f"   Order: {order1.id} - Status: {order1.status}")
    
    print("\n✅ Database seeding completed successfully!")
    print("\n🚀 You can now:")
    print("   1. Start the server: python manage.py runserver")
    print("   2. Visit GraphiQL: http://127.0.0.1:8000/graphql")
    print("   3. Visit Admin: http://127.0.0.1:8000/admin")
    print("   4. Try the sample queries from the README")


if __name__ == "__main__":
    create_sample_data() 