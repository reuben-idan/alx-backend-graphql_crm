import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django_filters import FilterSet, OrderingFilter
from django.db.models import Q
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
    phone = graphene.String(required=True)
    address = graphene.String(required=True)


class UpdateCustomerInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    address = graphene.String()


class CreateProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    stock_quantity = graphene.Int(required=True)
    sku = graphene.String(required=True)


class UpdateProductInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String()
    description = graphene.String()
    price = graphene.Decimal()
    stock_quantity = graphene.Int()
    sku = graphene.String()


class CreateOrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    status = graphene.String()
    shipping_address = graphene.String(required=True)
    notes = graphene.String()


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
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)


class UpdateCustomerPayload(graphene.ObjectType):
    customer = graphene.Field(CustomerType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)


class DeleteCustomerPayload(graphene.ObjectType):
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)


class CreateProductPayload(graphene.ObjectType):
    product = graphene.Field(ProductType)
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
    errors = graphene.List(graphene.String)


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
            customer = Customer.objects.create(
                name=input.name,
                email=input.email,
                phone=input.phone,
                address=input.address
            )
            return CreateCustomerPayload(customer=customer, success=True, errors=[])
        except Exception as e:
            return CreateCustomerPayload(customer=None, success=False, errors=[str(e)])


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
            product = Product.objects.create(
                name=input.name,
                description=input.description,
                price=input.price,
                stock_quantity=input.stock_quantity,
                sku=input.sku
            )
            return CreateProductPayload(product=product, success=True, errors=[])
        except Exception as e:
            return CreateProductPayload(product=None, success=False, errors=[str(e)])


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
            customer = Customer.objects.get(id=input.customer_id)
            order = Order.objects.create(
                customer=customer,
                status=input.status or 'pending',
                shipping_address=input.shipping_address,
                notes=input.notes or ''
            )
            return CreateOrderPayload(order=order, success=True, errors=[])
        except Customer.DoesNotExist:
            return CreateOrderPayload(order=None, success=False, errors=["Customer not found"])
        except Exception as e:
            return CreateOrderPayload(order=None, success=False, errors=[str(e)])


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