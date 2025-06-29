from django.contrib import admin
from .models import Customer, Product, Order, OrderItem


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'total_orders', 'total_spent', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['id', 'created_at', 'updated_at', 'total_orders', 'total_spent']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Address', {
            'fields': ('address',)
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'price', 'stock_quantity', 'is_in_stock', 'created_at']
    list_filter = ['created_at', 'is_in_stock']
    search_fields = ['name', 'sku', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'is_in_stock']
    ordering = ['name']
    
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'description', 'sku')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock_quantity')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'total_amount', 'item_count', 'order_date']
    list_filter = ['status', 'order_date', 'created_at']
    search_fields = ['customer__name', 'customer__email', 'id']
    readonly_fields = ['id', 'created_at', 'updated_at', 'total_amount', 'item_count']
    ordering = ['-order_date']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('customer', 'status', 'order_date')
        }),
        ('Shipping', {
            'fields': ('shipping_address', 'notes')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price', 'subtotal']
    list_filter = ['order__status', 'order__order_date']
    search_fields = ['order__id', 'product__name']
    readonly_fields = ['id', 'subtotal']
    ordering = ['-order__order_date']
    
    fieldsets = (
        ('Item Information', {
            'fields': ('order', 'product', 'quantity', 'unit_price')
        }),
        ('System Information', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    ) 