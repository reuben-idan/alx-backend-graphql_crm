import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django_filters import FilterSet, OrderingFilter
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Customer, Product, Order, OrderItem
from .filters import CustomerFilter, ProductFilter, OrderFilter


# GraphQL Types
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        interfaces = (graphene.relay.Node,)
        fields = '__all__'
        filterset_class = CustomerFilter


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        interfaces = (graphene.relay.Node,)
        fields = '__all__'
        filterset_class = ProductFilter


class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        interfaces = (graphene.relay.Node,)
        fields = '__all__'


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        interfaces = (graphene.relay.Node,)
        fields = '__all__'
        filterset_class = OrderFilter


# Input Types for Filtering
class CustomerFilterInput(graphene.InputObjectType):
    name = graphene.String()
    name_icontains = graphene.String()
    email = graphene.String()
    email_icontains = graphene.String()
    phone = graphene.String()
    phone_icontains = graphene.String()
    phone_pattern = graphene.String()
    created_at_gte = graphene.DateTime()
    created_at_lte = graphene.DateTime()
    order_by = graphene.String()


class ProductFilterInput(graphene.InputObjectType):
    name = graphene.String()
    name_icontains = graphene.String()
    price_gte = graphene.Decimal()
    price_lte = graphene.Decimal()
    stock_gte = graphene.Int()
    stock_lte = graphene.Int()
    low_stock = graphene.Boolean()
    order_by = graphene.String()


class OrderFilterInput(graphene.InputObjectType):
    total_amount_gte = graphene.Decimal()
    total_amount_lte = graphene.Decimal()
    order_date_gte = graphene.DateTime()
    order_date_lte = graphene.DateTime()
    customer_name = graphene.String()
    product_name = graphene.String()
    product_id = graphene.String()
    order_by = graphene.String()


# Input Types for Mutations
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
    price = graphene.Decimal(required=True)
    stock = graphene.Int()


class CreateOrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime()


# Payload Types
class CreateCustomerPayload(graphene.ObjectType):
    customer = graphene.Field(CustomerType)
    message = graphene.String()
    success = graphene.Boolean()


class BulkCreateCustomersPayload(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()


class CreateProductPayload(graphene.ObjectType):
    product = graphene.Field(ProductType)
    success = graphene.Boolean()
    message = graphene.String()


class CreateOrderPayload(graphene.ObjectType):
    order = graphene.Field(OrderType)
    success = graphene.Boolean()
    message = graphene.String()


class UpdateLowStockProductsPayload(graphene.ObjectType):
    updated_products = graphene.List(ProductType)
    success = graphene.Boolean()
    message = graphene.String()


# Mutations
class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CreateCustomerInput(required=True)
    
    Output = CreateCustomerPayload
    
    def mutate(self, info, input):
        try:
            # Validate email uniqueness
            if Customer.objects.filter(email=input.email).exists():
                return CreateCustomerPayload(
                    customer=None,
                    message="Email already exists",
                    success=False
                )
            
            # Validate phone format if provided
            if input.phone:
                import re
                phone_pattern = r'^(\+?1?\d{9,15}|(\d{3}-){2}\d{4})$'
                if not re.match(phone_pattern, input.phone):
                    return CreateCustomerPayload(
                        customer=None,
                        message="Invalid phone format. Use +1234567890 or 123-456-7890",
                        success=False
                    )
            
            customer = Customer.objects.create(
                name=input.name,
                email=input.email,
                phone=input.phone or None
            )
            
            return CreateCustomerPayload(
                customer=customer,
                message="Customer created successfully",
                success=True
            )
            
        except Exception as e:
            return CreateCustomerPayload(
                customer=None,
                message=f"Error creating customer: {str(e)}",
                success=False
            )


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(BulkCreateCustomerInput, required=True)
    
    Output = BulkCreateCustomersPayload
    
    def mutate(self, info, input):
        customers = []
        errors = []
        
        with transaction.atomic():
            for customer_data in input:
                try:
                    # Validate email uniqueness
                    if Customer.objects.filter(email=customer_data.email).exists():
                        errors.append(f"Email {customer_data.email} already exists")
                        continue
                    
                    # Validate phone format if provided
                    if customer_data.phone:
                        import re
                        phone_pattern = r'^(\+?1?\d{9,15}|(\d{3}-){2}\d{4})$'
                        if not re.match(phone_pattern, customer_data.phone):
                            errors.append(f"Invalid phone format for {customer_data.email}")
                            continue
                    
                    customer = Customer.objects.create(
                        name=customer_data.name,
                        email=customer_data.email,
                        phone=customer_data.phone or None
                    )
                    customers.append(customer)
                    
                except Exception as e:
                    errors.append(f"Error creating {customer_data.email}: {str(e)}")
        
        return BulkCreateCustomersPayload(
            customers=customers,
            errors=errors,
            success=len(errors) == 0
        )


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = CreateProductInput(required=True)
    
    Output = CreateProductPayload
    
    def mutate(self, info, input):
        try:
            # Validate price is positive
            if input.price <= 0:
                return CreateProductPayload(
                    product=None,
                    message="Price must be positive",
                    success=False
                )
            
            # Validate stock is not negative
            stock = input.stock or 0
            if stock < 0:
                return CreateProductPayload(
                    product=None,
                    message="Stock cannot be negative",
                    success=False
                )
            
            product = Product.objects.create(
                name=input.name,
                price=input.price,
                stock=stock
            )
            
            return CreateProductPayload(
                product=product,
                message="Product created successfully",
                success=True
            )
            
        except Exception as e:
            return CreateProductPayload(
                product=None,
                message=f"Error creating product: {str(e)}",
                success=False
            )


class CreateOrder(graphene.Mutation):
    class Arguments:
        input = CreateOrderInput(required=True)
    
    Output = CreateOrderPayload
    
    def mutate(self, info, input):
        try:
            # Validate customer exists
            try:
                customer = Customer.objects.get(id=input.customer_id)
            except Customer.DoesNotExist:
                return CreateOrderPayload(
                    order=None,
                    message="Invalid customer ID",
                    success=False
                )
            
            # Validate at least one product
            if not input.product_ids:
                return CreateOrderPayload(
                    order=None,
                    message="At least one product must be selected",
                    success=False
                )
            
            # Validate products exist
            products = []
            for product_id in input.product_ids:
                try:
                    product = Product.objects.get(id=product_id)
                    products.append(product)
                except Product.DoesNotExist:
                    return CreateOrderPayload(
                        order=None,
                        message=f"Invalid product ID: {product_id}",
                        success=False
                    )
            
            # Create order
            order = Order.objects.create(
                customer=customer,
                order_date=input.order_date or None
            )
            
            # Add products to order
            total_amount = 0
            for product in products:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    unit_price=product.price
                )
                total_amount += product.price
            
            # Update order total
            order.total_amount = total_amount
            order.save()
            
            return CreateOrderPayload(
                order=order,
                message="Order created successfully",
                success=True
            )
            
        except Exception as e:
            return CreateOrderPayload(
                order=None,
                message=f"Error creating order: {str(e)}",
                success=False
            )


class UpdateLowStockProducts(graphene.Mutation):
    Output = UpdateLowStockProductsPayload
    
    def mutate(self, info):
        try:
            # Query products with stock < 10
            low_stock_products = Product.objects.filter(stock__lt=10)
            
            if not low_stock_products.exists():
                return UpdateLowStockProductsPayload(
                    updated_products=[],
                    success=True,
                    message="No low stock products found"
                )
            
            # Increment stock by 10 for each low stock product
            updated_products = []
            for product in low_stock_products:
                product.stock += 10
                product.save()
                updated_products.append(product)
            
            return UpdateLowStockProductsPayload(
                updated_products=updated_products,
                success=True,
                message=f"Successfully updated {len(updated_products)} low stock products"
            )
            
        except Exception as e:
            return UpdateLowStockProductsPayload(
                updated_products=[],
                success=False,
                message=f"Error updating low stock products: {str(e)}"
            )


# Query Class
class Query(graphene.ObjectType):
    # Basic queries
    customers = graphene.List(CustomerType)
    products = graphene.List(ProductType)
    orders = graphene.List(OrderType)
    customer = graphene.Field(CustomerType, id=graphene.ID(required=True))
    product = graphene.Field(ProductType, id=graphene.ID(required=True))
    order = graphene.Field(OrderType, id=graphene.ID(required=True))
    
    # Filtered queries with Relay connections
    all_customers = DjangoFilterConnectionField(CustomerType)
    all_products = DjangoFilterConnectionField(ProductType)
    all_orders = DjangoFilterConnectionField(OrderType)
    
    # Custom filtered queries
    filtered_customers = graphene.List(
        CustomerType,
        filter=graphene.Argument(CustomerFilterInput)
    )
    
    filtered_products = graphene.List(
        ProductType,
        filter=graphene.Argument(ProductFilterInput)
    )
    
    filtered_orders = graphene.List(
        OrderType,
        filter=graphene.Argument(OrderFilterInput)
    )
    
    def resolve_customers(self, info):
        return Customer.objects.all()
    
    def resolve_products(self, info):
        return Product.objects.all()
    
    def resolve_orders(self, info):
        return Order.objects.all()
    
    def resolve_customer(self, info, id):
        try:
            return Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return None
    
    def resolve_product(self, info, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            return None
    
    def resolve_order(self, info, id):
        try:
            return Order.objects.get(id=id)
        except Order.DoesNotExist:
            return None
    
    def resolve_filtered_customers(self, info, filter=None):
        queryset = Customer.objects.all()
        
        if filter:
            if filter.name:
                queryset = queryset.filter(name__icontains=filter.name)
            if filter.name_icontains:
                queryset = queryset.filter(name__icontains=filter.name_icontains)
            if filter.email:
                queryset = queryset.filter(email__icontains=filter.email)
            if filter.email_icontains:
                queryset = queryset.filter(email__icontains=filter.email_icontains)
            if filter.phone:
                queryset = queryset.filter(phone__icontains=filter.phone)
            if filter.phone_icontains:
                queryset = queryset.filter(phone__icontains=filter.phone_icontains)
            if filter.phone_pattern:
                queryset = queryset.filter(phone__startswith=filter.phone_pattern)
            if filter.created_at_gte:
                queryset = queryset.filter(created_at__gte=filter.created_at_gte)
            if filter.created_at_lte:
                queryset = queryset.filter(created_at__lte=filter.created_at_lte)
            if filter.order_by:
                queryset = queryset.order_by(filter.order_by)
        
        return queryset
    
    def resolve_filtered_products(self, info, filter=None):
        queryset = Product.objects.all()
        
        if filter:
            if filter.name:
                queryset = queryset.filter(name__icontains=filter.name)
            if filter.name_icontains:
                queryset = queryset.filter(name__icontains=filter.name_icontains)
            if filter.price_gte:
                queryset = queryset.filter(price__gte=filter.price_gte)
            if filter.price_lte:
                queryset = queryset.filter(price__lte=filter.price_lte)
            if filter.stock_gte:
                queryset = queryset.filter(stock__gte=filter.stock_gte)
            if filter.stock_lte:
                queryset = queryset.filter(stock__lte=filter.stock_lte)
            if filter.low_stock:
                queryset = queryset.filter(stock__lt=10)
            if filter.order_by:
                queryset = queryset.order_by(filter.order_by)
        
        return queryset
    
    def resolve_filtered_orders(self, info, filter=None):
        queryset = Order.objects.all()
        
        if filter:
            if filter.total_amount_gte:
                queryset = queryset.filter(total_amount__gte=filter.total_amount_gte)
            if filter.total_amount_lte:
                queryset = queryset.filter(total_amount__lte=filter.total_amount_lte)
            if filter.order_date_gte:
                queryset = queryset.filter(order_date__gte=filter.order_date_gte)
            if filter.order_date_lte:
                queryset = queryset.filter(order_date__lte=filter.order_date_lte)
            if filter.customer_name:
                queryset = queryset.filter(customer__name__icontains=filter.customer_name)
            if filter.product_name:
                queryset = queryset.filter(items__product__name__icontains=filter.product_name).distinct()
            if filter.product_id:
                queryset = queryset.filter(items__product__id=filter.product_id).distinct()
            if filter.order_by:
                queryset = queryset.order_by(filter.order_by)
        
        return queryset


# Mutation Class
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
    update_low_stock_products = UpdateLowStockProducts.Field() 