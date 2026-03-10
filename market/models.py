from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
try:
    from django.contrib.postgres.indexes import GinIndex
except ImportError:
    GinIndex = None

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    brand = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    old_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Rasm uchun URL (agar fayl yuklanmasa)")
    rating = models.FloatField(default=0)
    reviews_count = models.IntegerField(default=0)
    stock = models.IntegerField(default=10)
    is_new = models.BooleanField(default=False)

    @property
    def get_image(self):
        if self.image_url:
            return self.image_url
        if self.image:
            return self.image.url
        return "https://via.placeholder.com/500x650?text=No+Image"
    keywords = models.TextField(blank=True, null=True, help_text="Search keywords and synonyms (e.g. 'donak, magiz' for apricot kernels)")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            # Note: GIN index requires PostgreSQL. Won't affect SQLite dev env.
            GinIndex(fields=['name'], name='product_name_gin') if GinIndex else models.Index(fields=['name']),
            models.Index(fields=['brand'], name='product_brand_idx'),
        ]

    def __str__(self):
        return self.name

    @property
    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return round(((self.old_price - self.price) / self.old_price) * 100)
        return 0

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    guest_uuid = models.UUIDField(null=True, blank=True, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    @property
    def total_price(self):
        return self.product.price * self.quantity

class Banner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='banners/')
    link = models.CharField(max_length=200, default='#')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']

class Profile(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Telefon raqami '+998901234567' formatida bo'lishi kerak.")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(validators=[phone_regex], max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - Profile"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    guest_uuid = models.UUIDField(null=True, blank=True, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} favorited"

class Order(models.Model):
    STATUS_CHOICES = [
        ('yangi', 'Yangi'),
        ('tasdiqlangan', 'Tasdiqlangan'),
        ('bekor', 'Bekor qilingan'),
        ('kuryer', 'Kuryerda'),
        ('yetkazildi', 'Yetkazib berildi'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    guest_uuid = models.UUIDField(null=True, blank=True, db_index=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')], max_length=20)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='yangi')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    user_note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.price * self.quantity

# Signals to auto-create profile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)
