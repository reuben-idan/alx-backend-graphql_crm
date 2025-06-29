import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Q
import re
from .models import Customer, Product, Order, OrderItem
from .filters import CustomerFilter, ProductFilter, OrderFilter
from graphql_relay import from_global_id

# Types
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = '__all__'
        filterset_class = CustomerFilter
        interfaces = (graphene.relay.Node,)

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = '__all__'
        filterset_class = ProductFilter
        interfaces = (graphene.relay.Node,)

class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = '__all__'
        filterset_class = OrderFilter
        interfaces = (graphene.relay.Node,)

# Input Types
class CreateCustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class BulkCreateCustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class CreateProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.String(required=True)  # Changed to String for Decimal
    stock = graphene.Int()

class CreateOrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime()

# Response Types
class CreateCustomerResponse(graphene.ObjectType):
    customer = graphene.Field(CustomerType)
    message = graphene.String()
    success = graphene.Boolean()

class BulkCreateCustomersResponse(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

class CreateProductResponse(graphene.ObjectType):
    product = graphene.Field(ProductType)
    message = graphene.String()
    success = graphene.Boolean()

class CreateOrderResponse(graphene.ObjectType):
    order = graphene.Field(OrderType)
    message = graphene.String()
    success = graphene.Boolean()

# Mutations
class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CreateCustomerInput(required=True)

    Output = CreateCustomerResponse

    def mutate(self, info, input):
        try:
            # Validate email uniqueness
            if Customer.objects.filter(email=input.email).exists():
                return CreateCustomerResponse(
                    customer=None,
                    message="Email already exists",
                    success=False
                )

            # Validate phone format if provided (more flexible)
            if input.phone:
                phone_pattern = r'^[\+]?[1-9][\d]{0,15}$'
                if not re.match(phone_pattern, input.phone.replace('-', '').replace(' ', '')):
                    return CreateCustomerResponse(
                        customer=None,
                        message="Invalid phone number format",
                        success=False
                    )

            customer = Customer.objects.create(
                name=input.name,
                email=input.email,
                phone=input.phone
            )

            return CreateCustomerResponse(
                customer=customer,
                message="Customer created successfully",
                success=True
            )

        except Exception as e:
            return CreateCustomerResponse(
                customer=None,
                message=str(e),
                success=False
            )

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CreateCustomerInput, required=True)

    Output = BulkCreateCustomersResponse

    @transaction.atomic
    def mutate(self, info, input):
        customers = []
        errors = []

        for customer_input in input:
            try:
                # Validate email uniqueness
                if Customer.objects.filter(email=customer_input.email).exists():
                    errors.append(f"Email {customer_input.email} already exists")
                    continue

                # Validate phone format if provided (more flexible)
                if customer_input.phone:
                    phone_pattern = r'^[\+]?[1-9][\d]{0,15}$'
                    if not re.match(phone_pattern, customer_input.phone.replace('-', '').replace(' ', '')):
                        errors.append(f"Invalid phone format for {customer_input.email}")
                        continue

                customer = Customer.objects.create(
                    name=customer_input.name,
                    email=customer_input.email,
                    phone=customer_input.phone
                )
                customers.append(customer)

            except Exception as e:
                errors.append(f"Error creating customer {customer_input.email}: {str(e)}")

        return BulkCreateCustomersResponse(
            customers=customers,
            errors=errors,
            success=len(errors) == 0
        )

class CreateProduct(graphene.Mutation):
    class Arguments:
        input = CreateProductInput(required=True)

    Output = CreateProductResponse

    def mutate(self, info, input):
        try:
            # Convert string to Decimal
            from decimal import Decimal
            price = Decimal(input.price)
            
            # Validate price is positive
            if price <= 0:
                return CreateProductResponse(
                    product=None,
                    message="Price must be positive",
                    success=False
                )

            # Validate stock is non-negative
            stock = input.stock if input.stock is not None else 0
            if stock < 0:
                return CreateProductResponse(
                    product=None,
                    message="Stock cannot be negative",
                    success=False
                )

            product = Product.objects.create(
                name=input.name,
                price=price,
                stock=stock
            )

            return CreateProductResponse(
                product=product,
                message="Product created successfully",
                success=True
            )

        except Exception as e:
            return CreateProductResponse(
                product=None,
                message=str(e),
                success=False
            )

class CreateOrder(graphene.Mutation):
    class Arguments:
        input = CreateOrderInput(required=True)

    Output = CreateOrderResponse

    @transaction.atomic
    def mutate(self, info, input):
        try:
            # Convert Relay ID to database ID for customer
            try:
                customer_type, customer_db_id = from_global_id(input.customer_id)
                customer = Customer.objects.get(id=customer_db_id)
            except (ValueError, Customer.DoesNotExist):
                return CreateOrderResponse(
                    order=None,
                    message="Customer not found",
                    success=False
                )

            # Validate products exist and get them
            products = []
            for product_relay_id in input.product_ids:
                try:
                    product_type, product_db_id = from_global_id(product_relay_id)
                    product = Product.objects.get(id=product_db_id)
                    products.append(product)
                except (ValueError, Product.DoesNotExist):
                    return CreateOrderResponse(
                        order=None,
                        message=f"Product with ID {product_relay_id} not found",
                        success=False
                    )

            if not products:
                return CreateOrderResponse(
                    order=None,
                    message="At least one product must be selected",
                    success=False
                )

            # Calculate total amount
            total_amount = sum(product.price for product in products)

            # Create order
            order = Order.objects.create(
                customer=customer,
                total_amount=total_amount
            )

            # Create order items
            for product in products:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=1,
                    price=product.price
                )

            return CreateOrderResponse(
                order=order,
                message="Order created successfully",
                success=True
            )

        except Exception as e:
            return CreateOrderResponse(
                order=None,
                message=str(e),
                success=False
            )

# Queries
class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")
    
    # Customer queries with filtering
    all_customers = DjangoFilterConnectionField(CustomerType)
    customer = graphene.Field(CustomerType, id=graphene.ID(required=True))
    
    # Product queries with filtering
    all_products = DjangoFilterConnectionField(ProductType)
    product = graphene.Field(ProductType, id=graphene.ID(required=True))
    
    # Order queries with filtering
    all_orders = DjangoFilterConnectionField(OrderType)
    order = graphene.Field(OrderType, id=graphene.ID(required=True))

    def resolve_customer(self, info, id):
        try:
            customer_type, customer_db_id = from_global_id(id)
            return Customer.objects.get(id=customer_db_id)
        except (ValueError, Customer.DoesNotExist):
            return None

    def resolve_product(self, info, id):
        try:
            product_type, product_db_id = from_global_id(id)
            return Product.objects.get(id=product_db_id)
        except (ValueError, Product.DoesNotExist):
            return None

    def resolve_order(self, info, id):
        try:
            order_type, order_db_id = from_global_id(id)
            return Order.objects.get(id=order_db_id)
        except (ValueError, Order.DoesNotExist):
            return None

# Mutation class
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field() 