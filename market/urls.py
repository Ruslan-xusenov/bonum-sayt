from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

app_name = 'market'

router = DefaultRouter()
router.register(r'products', api_views.ProductViewSet, basename='api_product')
router.register(r'categories', api_views.CategoryViewSet, basename='api_category')
router.register(r'cart', api_views.CartItemViewSet, basename='api_cart')
router.register(r'orders', api_views.OrderViewSet, basename='api_order')
router.register(r'banners', api_views.BannerViewSet, basename='api_banner')

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Admin Dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/product/add/', views.admin_add_product, name='admin_add_product'),
    path('dashboard/product/edit/<int:pk>/', views.admin_edit_product, name='admin_edit_product'),
    path('dashboard/product/delete/<int:pk>/', views.admin_delete_product, name='admin_delete_product'),
    
    # Banner Management
    path('dashboard/banner/add/', views.admin_add_banner, name='admin_add_banner'),
    path('dashboard/banner/edit/<int:pk>/', views.admin_edit_banner, name='admin_edit_banner'),
    path('dashboard/banner/delete/<int:pk>/', views.admin_delete_banner, name='admin_delete_banner'),
    
    # Category Management
    path('dashboard/category/add/', views.admin_add_category, name='admin_add_category'),
    path('dashboard/category/edit/<int:pk>/', views.admin_edit_category, name='admin_edit_category'),
    path('dashboard/category/delete/<int:pk>/', views.admin_delete_category, name='admin_delete_category'),
    path('dashboard/order/update/<int:pk>/<str:status>/', views.update_order_status, name='update_order_status'),
    path('profile/complete/', views.complete_profile, name='complete_profile'),
    path('favorite/toggle/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/get/', views.get_favorites, name='get_favorites'),
    
    # Custom API endpoints MUST come before router to avoid shadowing
    path('api/cart/add/<int:pk>/', views.api_add_to_cart, name='api_add_to_cart'),
    path('api/cart/update/<int:pk>/', views.api_update_cart_quantity, name='api_update_cart_quantity'),
    path('api/cart/get/', views.get_cart_items, name='get_cart_items'),
    path('api/profile/get/', views.get_user_profile, name='get_user_profile'),
    path('api/order/note/<int:pk>/', views.add_order_note, name='add_order_note'),
    path('api/profile/update/', views.update_profile_api, name='update_profile_api'),
    
    path('api/', include(router.urls)),
]
