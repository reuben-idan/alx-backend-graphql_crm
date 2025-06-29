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
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^(\+?1?\d{9,15}|(\d{3}-){2}\d{4})$',
                message="Phone number must be in format: '+1234567890' or '123-456-7890'"
            )
        ],
        help_text="Customer's phone number"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
    
    def __str__(self):
        return f"{self.name} ({self.email})"


class Product(models.Model):
    """Product model for storing product information."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, help_text="Product name")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Product price"
    )
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Available stock quantity"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return f"{self.name} - ${self.price}"


class Order(models.Model):
    """Order model for storing order information."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders',
        help_text="Customer who placed the order"
    )
    products = models.ManyToManyField(
        Product,
        through='OrderItem',
        related_name='orders',
        help_text="Products in this order"
    )
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Total amount of the order"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-order_date']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def __str__(self):
        return f"Order {self.id} - {self.customer.name}"
    
    def calculate_total(self):
        """Calculate total amount from order items."""
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        self.save()
        return total


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
        default=1,
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
        # Update order total
        self.order.calculate_total() 