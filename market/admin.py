from django.contrib import admin
from .models import Category, Product, Review, CartItem, Banner, Order, OrderItem, Profile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'rating')
    list_filter = ('category', 'is_new')
    search_fields = ('name', 'description', 'keywords')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_editable = ('is_active', 'order')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'total_price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'full_name', 'phone_number', 'address')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Buyurtma malumotlari', {
            'fields': ('status', 'total_amount', 'user_note')
        }),
        ('Mijoz malumotlari', {
            'fields': ('full_name', 'phone_number', 'address', 'user')
        }),
        ('Vaqt malumotlari', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number', 'address')

admin.site.register(Review)
admin.site.register(CartItem)
