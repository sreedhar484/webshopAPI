from django.urls import path
from .views import (
    ProductListCreateView, ProductDetailView,
    InventoryListView, InventoryDetailView,
    OrderListCreateView, OrderDetailView,
    PlaceOrderView
)

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    path('inventory/', InventoryListView.as_view(), name='inventory-list'),
    path('inventory/<int:pk>/', InventoryDetailView.as_view(), name='inventory-detail'),

    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('orders/place/', PlaceOrderView.as_view(), name='place-order'),
]
