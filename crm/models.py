from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone
import uuid


class Customer(models.Model):
    """Customer model for storing customer information."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, help_text="Customer's full name")
    email = models.EmailField(unique=True, help_text="Customer's email address")
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        help_text="Customer's phone number"
    )
    address = models.TextField(help_text="Customer's address")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    @property
    def total_orders(self):
        """Return the total number of orders for this customer."""
        return self.orders.count()
    
    @property
    def total_spent(self):
        """Return the total amount spent by this customer."""
        return sum(order.total_amount for order in self.orders.all())


class Product(models.Model):
    """Product model for storing product information."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, help_text="Product name")
    description = models.TextField(help_text="Product description")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Product price"
    )
    stock_quantity = models.PositiveIntegerField(
        default=0,
        help_text="Available stock quantity"
    )
    sku = models.CharField(
        max_length=50,
        unique=True,
        help_text="Stock Keeping Unit"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return f"{self.name} - ${self.price}"
    
    @property
    def is_in_stock(self):
        """Check if product is in stock."""
        return self.stock_quantity > 0


class Order(models.Model):
    """Order model for storing order information."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders',
        help_text="Customer who placed the order"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Order status"
    )
    order_date = models.DateTimeField(default=timezone.now)
    shipping_address = models.TextField(help_text="Shipping address")
    notes = models.TextField(blank=True, help_text="Additional notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-order_date']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def __str__(self):
        return f"Order {self.id} - {self.customer.name} ({self.status})"
    
    @property
    def total_amount(self):
        """Calculate the total amount for this order."""
        return sum(item.subtotal for item in self.items.all())
    
    @property
    def item_count(self):
        """Return the number of items in this order."""
        return self.items.count()


class OrderItem(models.Model):
    """OrderItem model for storing individual items in an order."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="Order this item belongs to"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        help_text="Product being ordered"
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Quantity of the product"
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Price per unit at the time of order"
    )
    
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        unique_together = ['order', 'product']
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Order {self.order.id}"
    
    @property
    def subtotal(self):
        """Calculate the subtotal for this item."""
        return self.quantity * self.unit_price
    
    def save(self, *args, **kwargs):
        """Override save to set unit_price if not provided."""
        if not self.unit_price:
            self.unit_price = self.product.price
        super().save(*args, **kwargs) 