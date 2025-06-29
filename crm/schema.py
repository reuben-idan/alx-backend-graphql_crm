import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django_filters import FilterSet, OrderingFilter
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Customer, Product, Order, OrderItem


# Filter Classes
class CustomerFilter(FilterSet):
    class Meta:
        model = Customer
        fields = {
            'name': ['icontains', 'exact'],
            'email': ['icontains', 'exact'],
            'phone': ['icontains', 'exact'],
        }
    
    order_by = OrderingFilter(
        fields=(
            ('name', 'name'),
            ('email', 'email'),
            ('created_at', 'created_at'),
        )
    )


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['icontains', 'exact'],
            'sku': ['icontains', 'exact'],
            'price': ['gte', 'lte', 'exact'],
            'stock_quantity': ['gte', 'lte', 'exact'],
        }
    
    order_by = OrderingFilter(
        fields=(
            ('name', 'name'),
            ('price', 'price'),
            ('stock_quantity', 'stock_quantity'),
            ('created_at', 'created_at'),
        )
    )


class OrderFilter(FilterSet):
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'customer__id': ['exact'],
            'order_date': ['gte', 'lte', 'exact'],
        }
    
    order_by = OrderingFilter(
        fields=(
            ('order_date', 'order_date'),
            ('status', 'status'),
            ('created_at', 'created_at'),
        )
    )


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
    price = graphene.Decimal(required=True)
    stock = graphene.Int()


class CreateOrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime()


class UpdateCustomerInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    address = graphene.String()


class UpdateProductInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String()
    description = graphene.String()
    price = graphene.Decimal()
    stock_quantity = graphene.Int()
    sku = graphene.String()


class UpdateOrderInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    status = graphene.String()
    shipping_address = graphene.String()
    notes = graphene.String()


class CreateOrderItemInput(graphene.InputObjectType):
    order_id = graphene.ID(required=True)
    product_id = graphene.ID(required=True)
    quantity = graphene.Int(required=True)
    unit_price = graphene.Decimal()


class UpdateOrderItemInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    quantity = graphene.Int()
    unit_price = graphene.Decimal()


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


class UpdateCustomerPayload(graphene.ObjectType):
    customer = graphene.Field(CustomerType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)


class DeleteCustomerPayload(graphene.ObjectType):
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)


class UpdateProductPayload(graphene.ObjectType):
    product = graphene.Field(ProductType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)


class DeleteProductPayload(graphene.ObjectType):
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)


class CreateOrderPayload(graphene.ObjectType):
    order = graphene.Field(OrderType)
    success = graphene.Boolean()
    message = graphene.String()


class UpdateOrderPayload(graphene.ObjectType):
    order = graphene.Field(OrderType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)


class DeleteOrderPayload(graphene.ObjectType):
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)


class CreateOrderItemPayload(graphene.ObjectType):
    order_item = graphene.Field(OrderItemType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)


class UpdateOrderItemPayload(graphene.ObjectType):
    order_item = graphene.Field(OrderItemType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)


class DeleteOrderItemPayload(graphene.ObjectType):
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)


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


class UpdateCustomer(graphene.Mutation):
    class Arguments:
        input = UpdateCustomerInput(required=True)
    
    Output = UpdateCustomerPayload
    
    def mutate(self, info, input):
        try:
            customer = Customer.objects.get(id=input.id)
            
            if input.name is not None:
                customer.name = input.name
            if input.email is not None:
                customer.email = input.email
            if input.phone is not None:
                customer.phone = input.phone
            if input.address is not None:
                customer.address = input.address
            
            customer.save()
            return UpdateCustomerPayload(customer=customer, success=True, errors=[])
        except Customer.DoesNotExist:
            return UpdateCustomerPayload(customer=None, success=False, errors=["Customer not found"])
        except Exception as e:
            return UpdateCustomerPayload(customer=None, success=False, errors=[str(e)])


class DeleteCustomer(graphene.Mutation):
    class Arguments:
        input = graphene.ID(required=True)
    
    Output = DeleteCustomerPayload
    
    def mutate(self, info, input):
        try:
            customer = Customer.objects.get(id=input)
            customer.delete()
            return DeleteCustomerPayload(success=True, errors=[])
        except Customer.DoesNotExist:
            return DeleteCustomerPayload(success=False, errors=["Customer not found"])
        except Exception as e:
            return DeleteCustomerPayload(success=False, errors=[str(e)])


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


class UpdateProduct(graphene.Mutation):
    class Arguments:
        input = UpdateProductInput(required=True)
    
    Output = UpdateProductPayload
    
    def mutate(self, info, input):
        try:
            product = Product.objects.get(id=input.id)
            
            if input.name is not None:
                product.name = input.name
            if input.description is not None:
                product.description = input.description
            if input.price is not None:
                product.price = input.price
            if input.stock_quantity is not None:
                product.stock_quantity = input.stock_quantity
            if input.sku is not None:
                product.sku = input.sku
            
            product.save()
            return UpdateProductPayload(product=product, success=True, errors=[])
        except Product.DoesNotExist:
            return UpdateProductPayload(product=None, success=False, errors=["Product not found"])
        except Exception as e:
            return UpdateProductPayload(product=None, success=False, errors=[str(e)])


class DeleteProduct(graphene.Mutation):
    class Arguments:
        input = graphene.ID(required=True)
    
    Output = DeleteProductPayload
    
    def mutate(self, info, input):
        try:
            product = Product.objects.get(id=input)
            product.delete()
            return DeleteProductPayload(success=True, errors=[])
        except Product.DoesNotExist:
            return DeleteProductPayload(success=False, errors=["Product not found"])
        except Exception as e:
            return DeleteProductPayload(success=False, errors=[str(e)])


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


class UpdateOrder(graphene.Mutation):
    class Arguments:
        input = UpdateOrderInput(required=True)
    
    Output = UpdateOrderPayload
    
    def mutate(self, info, input):
        try:
            order = Order.objects.get(id=input.id)
            
            if input.status is not None:
                order.status = input.status
            if input.shipping_address is not None:
                order.shipping_address = input.shipping_address
            if input.notes is not None:
                order.notes = input.notes
            
            order.save()
            return UpdateOrderPayload(order=order, success=True, errors=[])
        except Order.DoesNotExist:
            return UpdateOrderPayload(order=None, success=False, errors=["Order not found"])
        except Exception as e:
            return UpdateOrderPayload(order=None, success=False, errors=[str(e)])


class DeleteOrder(graphene.Mutation):
    class Arguments:
        input = graphene.ID(required=True)
    
    Output = DeleteOrderPayload
    
    def mutate(self, info, input):
        try:
            order = Order.objects.get(id=input)
            order.delete()
            return DeleteOrderPayload(success=True, errors=[])
        except Order.DoesNotExist:
            return DeleteOrderPayload(success=False, errors=["Order not found"])
        except Exception as e:
            return DeleteOrderPayload(success=False, errors=[str(e)])


class CreateOrderItem(graphene.Mutation):
    class Arguments:
        input = CreateOrderItemInput(required=True)
    
    Output = CreateOrderItemPayload
    
    def mutate(self, info, input):
        try:
            order = Order.objects.get(id=input.order_id)
            product = Product.objects.get(id=input.product_id)
            
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=input.quantity,
                unit_price=input.unit_price or product.price
            )
            return CreateOrderItemPayload(order_item=order_item, success=True, errors=[])
        except (Order.DoesNotExist, Product.DoesNotExist) as e:
            return CreateOrderItemPayload(order_item=None, success=False, errors=[str(e)])
        except Exception as e:
            return CreateOrderItemPayload(order_item=None, success=False, errors=[str(e)])


class UpdateOrderItem(graphene.Mutation):
    class Arguments:
        input = UpdateOrderItemInput(required=True)
    
    Output = UpdateOrderItemPayload
    
    def mutate(self, info, input):
        try:
            order_item = OrderItem.objects.get(id=input.id)
            
            if input.quantity is not None:
                order_item.quantity = input.quantity
            if input.unit_price is not None:
                order_item.unit_price = input.unit_price
            
            order_item.save()
            return UpdateOrderItemPayload(order_item=order_item, success=True, errors=[])
        except OrderItem.DoesNotExist:
            return UpdateOrderItemPayload(order_item=None, success=False, errors=["Order item not found"])
        except Exception as e:
            return UpdateOrderItemPayload(order_item=None, success=False, errors=[str(e)])


class DeleteOrderItem(graphene.Mutation):
    class Arguments:
        input = graphene.ID(required=True)
    
    Output = DeleteOrderItemPayload
    
    def mutate(self, info, input):
        try:
            order_item = OrderItem.objects.get(id=input)
            order_item.delete()
            return DeleteOrderItemPayload(success=True, errors=[])
        except OrderItem.DoesNotExist:
            return DeleteOrderItemPayload(success=False, errors=["Order item not found"])
        except Exception as e:
            return DeleteOrderItemPayload(success=False, errors=[str(e)])


# Query Class
class Query(graphene.ObjectType):
    # Customer queries
    customer = graphene.Field(CustomerType, id=graphene.ID(required=True))
    customers = DjangoFilterConnectionField(CustomerType)
    
    # Product queries
    product = graphene.Field(ProductType, id=graphene.ID(required=True))
    products = DjangoFilterConnectionField(ProductType)
    
    # Order queries
    order = graphene.Field(OrderType, id=graphene.ID(required=True))
    orders = DjangoFilterConnectionField(OrderType)
    
    # Order item queries
    order_item = graphene.Field(OrderItemType, id=graphene.ID(required=True))
    
    # Search queries
    search_customers = graphene.List(CustomerType, query=graphene.String(required=True))
    search_products = graphene.List(ProductType, query=graphene.String(required=True))
    
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
    
    def resolve_order_item(self, info, id):
        try:
            return OrderItem.objects.get(id=id)
        except OrderItem.DoesNotExist:
            return None
    
    def resolve_search_customers(self, info, query):
        return Customer.objects.filter(
            Q(name__icontains=query) | 
            Q(email__icontains=query) | 
            Q(phone__icontains=query)
        )
    
    def resolve_search_products(self, info, query):
        return Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(sku__icontains=query)
        )


# Mutation Class
class Mutation(graphene.ObjectType):
    # Customer mutations
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    update_customer = UpdateCustomer.Field()
    delete_customer = DeleteCustomer.Field()
    
    # Product mutations
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()
    
    # Order mutations
    create_order = CreateOrder.Field()
    update_order = UpdateOrder.Field()
    delete_order = DeleteOrder.Field()
    
    # Order item mutations
    create_order_item = CreateOrderItem.Field()
    update_order_item = UpdateOrderItem.Field()
    delete_order_item = DeleteOrderItem.Field()


# Schema
schema = graphene.Schema(query=Query, mutation=Mutation) 