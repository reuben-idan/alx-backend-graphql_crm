from django.contrib import admin
from .models import Customer, Product, Order, OrderItem


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Product Information', {
            'fields': ('name',)
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = []


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'total_amount', 'order_date']
    list_filter = ['order_date', 'created_at']
    search_fields = ['customer__name', 'customer__email', 'id']
    readonly_fields = ['id', 'created_at', 'updated_at', 'total_amount']
    ordering = ['-order_date']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('customer', 'order_date')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at', 'total_amount'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price']
    list_filter = ['order__order_date']
    search_fields = ['order__id', 'product__name']
    readonly_fields = ['id']
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