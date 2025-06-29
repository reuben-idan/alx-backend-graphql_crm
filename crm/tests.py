from django.test import TestCase
from decimal import Decimal
from .models import Customer, Product, Order, OrderItem


class CustomerModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Test Customer",
            email="test@example.com",
            phone="+1234567890",
            address="123 Test St"
        )
    
    def test_customer_creation(self):
        self.assertEqual(self.customer.name, "Test Customer")
        self.assertEqual(self.customer.email, "test@example.com")
    
    def test_customer_str(self):
        self.assertEqual(str(self.customer), "Test Customer (test@example.com)")


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=Decimal("99.99"),
            stock_quantity=10,
            sku="TEST-001"
        )
    
    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, Decimal("99.99"))
    
    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product - $99.99")


class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Test Customer",
            email="test@example.com",
            phone="+1234567890",
            address="123 Test St"
        )
        
        self.order = Order.objects.create(
            customer=self.customer,
            status='pending',
            shipping_address="123 Test St"
        )
    
    def test_order_creation(self):
        self.assertEqual(self.order.customer, self.customer)
        self.assertEqual(self.order.status, 'pending') 