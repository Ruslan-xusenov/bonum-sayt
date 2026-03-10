from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.db.models import F
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from .models import Category, Product, Review, CartItem, Banner, Order
from .serializers import (
    CategorySerializer, ProductSerializer, ReviewSerializer, 
    CartItemSerializer, BannerSerializer, OrderSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().prefetch_related('subcategories')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @method_decorator(cache_page(60 * 15)) # 15 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @method_decorator(cache_page(60 * 5)) # 5 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        products = self.queryset.filter(name__icontains=query)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return CartItem.objects.filter(user=self.request.user)
        guest_uuid = getattr(self.request, 'guest_uuid', None)
        return CartItem.objects.filter(guest_uuid=guest_uuid) if guest_uuid else CartItem.objects.none()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            guest_uuid = getattr(self.request, 'guest_uuid', None)
            serializer.save(guest_uuid=guest_uuid)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.all().prefetch_related('items__product')
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    @transaction.atomic
    def perform_create(self, serializer):
        # 1. Save the order first
        order = serializer.save(user=self.request.user)
        
        # 2. Process items from cart
        cart_items = CartItem.objects.filter(user=self.request.user).select_related('product')
        
        if not cart_items.exists():
            raise serializers.ValidationError("Savatingiz bo'sh!")

        total_amount = 0
        for item in cart_items:
            # Atomic lock on product to prevent race condition
            product = Product.objects.select_for_update().get(pk=item.product.pk)
            
            if product.stock < item.quantity:
                # This will rollback the entire transaction
                raise serializers.ValidationError(f"{product.name} uchun yetarli mahsulot yo'q (Omborda: {product.stock})")
                
            # Create OrderItem
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price=product.price
            )
            
            # Update stock atomically
            product.stock = F('stock') - item.quantity
            product.save()
            
            total_amount += product.price * item.quantity
        
        # 3. Update final amount and clear cart
        order.total_amount = total_amount
        order.save()
        cart_items.delete()
        
        # 4. Clear cache to reflect stock changes
        cache.delete_pattern("views.decorators.cache.cache_page.*")

class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer
