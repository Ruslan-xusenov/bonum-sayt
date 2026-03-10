import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from market.models import Category, Product
from decimal import Decimal

# Get existing categories
electronics = Category.objects.get(name='Elektronika')
clothing = Category.objects.get(name='Kiyim')
home = Category.objects.get(name="Uy-ro'zg'or")
sports = Category.objects.get(name='Sport va dam olish')
beauty = Category.objects.get(name="Go'zallik va salomatlik")

# Additional products
additional_products = [
    {
        'name': 'MacBook Pro 14" M3 512GB',
        'description': 'Apple MacBook Pro 14-inch, M3 chip, 512GB SSD, 16GB RAM. Professional laptop for creative work.',
        'price': Decimal('24999000'),
        'old_price': Decimal('27999000'),
        'category': electronics,
        'rating': 4.9,
        'reviews_count': 450,
        'stock': 5,
        'is_new': True,
    },
    {
        'name': 'Samsung 55" QLED 4K Smart TV',
        'description': 'Samsung QLED 4K Smart TV, 55 inch, Quantum Processor, HDR10+, Tizen OS.',
        'price': Decimal('8999000'),
        'old_price': Decimal('10999000'),
        'category': electronics,
        'rating': 4.7,
        'reviews_count': 680,
        'stock': 12,
        'is_new': False,
    },
    {
        'name': 'Zara Erkaklar Kurtka',
        'description': 'Premium kurtka, 100% teri, klassik dizayn, qish uchun ideal.',
        'price': Decimal('1299000'),
        'old_price': None,
        'category': clothing,
        'rating': 4.4,
        'reviews_count': 210,
        'stock': 30,
        'is_new': False,
    },
    {
        'name': 'Puma Sportiv Kostyum',
        'description': 'Sportiv kostyum to\'plami, yuqori sifatli material, barcha o\'lchamlar mavjud.',
        'price': Decimal('599000'),
        'old_price': Decimal('799000'),
        'category': sports,
        'rating': 4.5,
        'reviews_count': 340,
        'stock': 45,
        'is_new': False,
    },
    {
        'name': 'Tefal Multivarka 5L',
        'description': 'Ko\'p funksiyali multivarka, 5 litr hajm, 12 dastur, avtomatik tayyorlash.',
        'price': Decimal('899000'),
        'old_price': Decimal('1199000'),
        'category': home,
        'rating': 4.6,
        'reviews_count': 520,
        'stock': 22,
        'is_new': False,
    },
    {
        'name': 'Xiaomi Mi Band 8 Smart Bilak',
        'description': 'Smart bilak, yurak urishi monitoringi, uyqu tahlili, 150+ sport rejimlari.',
        'price': Decimal('399000'),
        'old_price': None,
        'category': electronics,
        'rating': 4.5,
        'reviews_count': 890,
        'stock': 60,
        'is_new': True,
    },
    {
        'name': 'Nivea Yuz Parvarish To\'plami',
        'description': 'Kompleks yuz parvarish to\'plami, barcha teri turlari uchun, 5 mahsulot.',
        'price': Decimal('249000'),
        'old_price': Decimal('349000'),
        'category': beauty,
        'rating': 4.3,
        'reviews_count': 156,
        'stock': 80,
        'is_new': False,
    },
    {
        'name': 'Bosch Elektr Drel 750W',
        'description': 'Professional elektr drel, 750W quvvat, 13mm patron, kuchli moment.',
        'price': Decimal('1199000'),
        'old_price': None,
        'category': home,
        'rating': 4.7,
        'reviews_count': 280,
        'stock': 18,
        'is_new': False,
    },
    {
        'name': 'Canon EOS R50 Kamera',
        'description': 'Mirrorless kamera, 24.2MP, 4K video, RF mount, ideal boshlang\'ichlar uchun.',
        'price': Decimal('6999000'),
        'old_price': Decimal('7999000'),
        'category': electronics,
        'rating': 4.8,
        'reviews_count': 190,
        'stock': 8,
        'is_new': True,
    },
    {
        'name': 'Adidas Predator Futbol To\'pi',
        'description': 'Professional futbol to\'pi, FIFA tasdiqlangan, yuqori sifatli material.',
        'price': Decimal('299000'),
        'old_price': None,
        'category': sports,
        'rating': 4.6,
        'reviews_count': 420,
        'stock': 50,
        'is_new': False,
    },
]

print("Adding more products...")
for prod_data in additional_products:
    prod, created = Product.objects.get_or_create(
        name=prod_data['name'],
        defaults=prod_data
    )
    print(f"  {'Created' if created else 'Found'}: {prod.name}")

print(f"\nTotal products now: {Product.objects.count()}")
