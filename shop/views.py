from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Inventory, Order, OrderItem
from .serializers import ProductSerializer, InventorySerializer, OrderSerializer, OrderItemSerializer
from django.core.mail import send_mail
from django.conf import settings
# Product List and Detail Views
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Inventory Management Views
class InventoryListView(generics.ListCreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class InventoryDetailView(generics.RetrieveUpdateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

# Order Management Views
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# Place Order API
class PlaceOrderView(APIView):
    def post(self, request, *args, **kwargs):
        customer_name = request.data.get('customer_name')
        customer_email = request.data.get('customer_email')
        address = request.data.get('address')
        address_detail = address.split(",")
        payment_method=request.data.get('payment_method')
        items = request.data.get('items')

        if not items:
            return Response({"error": "Order must contain at least one item"}, status=status.HTTP_400_BAD_REQUEST)

        # Create Order
        order = Order.objects.create(customer_name=customer_name, customer_email=customer_email,address=address_detail[0],city=address_detail[1],zip_code=address_detail[2],country=address_detail[3],payment_method=payment_method)

        # Process Items
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity')

            try:
                product = Product.objects.get(id=product_id)
                inventory = Inventory.objects.get(product=product)

                if inventory.stock_quantity < quantity:
                    return Response({"error": f"Insufficient stock for {product.name}"}, status=status.HTTP_400_BAD_REQUEST)

                # Deduct Stock and Save
                inventory.stock_quantity -= quantity
                inventory.save()

                # Create Order Item
                OrderItem.objects.create(order=order, product=product, quantity=quantity)

            except Product.DoesNotExist:
                return Response({"error": f"Product ID {product_id} not found"}, status=status.HTTP_404_NOT_FOUND)
            except Inventory.DoesNotExist:
                return Response({"error": f"Inventory for Product ID {product_id} not found"}, status=status.HTTP_404_NOT_FOUND)
        #self.send_order_email(order)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    def send_order_email(self, order):
        subject = "Order Confirmation - Your Order Has Been Placed"
        message = "Thank you for your order! Your order"
        recipient_email = order.customer_email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])