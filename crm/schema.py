# crm/schema.py
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Customer, Product, Order
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
import re
from .filters import CustomerFilter, ProductFilter, OrderFilter

# === Types ===
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter
        interfaces = (graphene.relay.Node,)

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        filterset_class = ProductFilter
        interfaces = (graphene.relay.Node,)

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilter
        interfaces = (graphene.relay.Node,)

# === Mutations ===
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise Exception("Email already exists")

        if phone and not re.match(r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$', phone):
            raise Exception("Invalid phone format")

        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer, message="Customer created successfully")

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(graphene.JSONString, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        customers = []
        errors = []
        with transaction.atomic():
            for i, data in enumerate(input):
                try:
                    if Customer.objects.filter(email=data['email']).exists():
                        raise Exception(f"Duplicate email: {data['email']}")
                    if 'phone' in data and data['phone'] and not re.match(r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$', data['phone']):
                        raise Exception(f"Invalid phone format: {data['phone']}")
                    customer = Customer(name=data['name'], email=data['email'], phone=data.get('phone'))
                    customer.full_clean()
                    customer.save()
                    customers.append(customer)
                except Exception as e:
                    errors.append(f"Row {i}: {str(e)}")
        return BulkCreateCustomers(customers=customers, errors=errors)

class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        stock = graphene.Int()

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise Exception("Price must be positive")
        if stock < 0:
            raise Exception("Stock cannot be negative")

        product = Product(name=name, price=price, stock=stock)
        product.save()
        return CreateProduct(product=product)

class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.DateTime()

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids, order_date=None):
        if not product_ids:
            raise Exception("At least one product must be selected")

        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise Exception("Invalid customer ID")

        products = []
        total = 0
        for pid in product_ids:
            try:
                product = Product.objects.get(pk=pid)
                products.append(product)
                total += product.price
            except Product.DoesNotExist:
                raise Exception(f"Invalid product ID: {pid}")

        order = Order(customer=customer, total_amount=total, order_date=order_date or timezone.now())
        order.save()
        order.products.set(products)
        return CreateOrder(order=order)

# === Schema Root ===
class Query(graphene.ObjectType):
    # ALX Required field
    hello = graphene.String(default_value="Hello, GraphQL!")
    
    # CRM functionality
    all_customers = DjangoFilterConnectionField(CustomerType)
    all_products = DjangoFilterConnectionField(ProductType)
    all_orders = DjangoFilterConnectionField(OrderType)

    def resolve_all_customers(self, info):
        return Customer.objects.all()

    def resolve_all_products(self, info):
        return Product.objects.all()

    def resolve_all_orders(self, info):
        return Order.objects.all()

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)