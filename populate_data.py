import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from market.models import Category, Product
from decimal import Decimal

# Create categories
categories_data = [
    {'name': 'Elektronika', 'icon': None},
    {'name': 'Kiyim', 'icon': None},
    {'name': 'Uy-ro\'zg\'or', 'icon': None},
    {'name': 'Sport va dam olish', 'icon': None},
    {'name': 'Go\'zallik va salomatlik', 'icon': None},
]

print("Creating categories...")
categories = {}
for cat_data in categories_data:
    cat, created = Category.objects.get_or_create(name=cat_data['name'], defaults=cat_data)
    categories[cat_data['name']] = cat
    print(f"  {'Created' if created else 'Found'}: {cat.name}")

# Create products
products_data = [
    {
        'name': 'Samsung Galaxy S23 Ultra 256GB',
        'description': 'Eng so\'nggi Samsung flagman telefoni. 200MP kamera, Snapdragon 8 Gen 2 protsessor, 6.8" Dynamic AMOLED ekran.',
        'price': Decimal('12999000'),
        'old_price': Decimal('14999000'),
        'category': categories['Elektronika'],
        'rating': 4.8,
        'reviews_count': 1250,
        'stock': 15,
        'is_new': True,
    },
    {
        'name': 'Apple iPhone 14 Pro 128GB',
        'description': 'iPhone 14 Pro - Dynamic Island, 48MP kamera, A16 Bionic chip, ProMotion texnologiyasi.',
        'price': Decimal('13999000'),
        'old_price': Decimal('15499000'),
        'category': categories['Elektronika'],
        'rating': 4.9,
        'reviews_count': 2100,
        'stock': 8,
        'is_new': True,
    },
    {
        'name': 'Nike Air Max 270 Krossovka',
        'description': 'Qulay va zamonaviy Nike krossovkasi. Havo yostig\'i texnologiyasi, yuqori sifatli materiallar.',
        'price': Decimal('899000'),
        'old_price': Decimal('1199000'),
        'category': categories['Sport va dam olish'],
        'rating': 4.6,
        'reviews_count': 450,
        'stock': 25,
        'is_new': False,
    },
    {
        'name': 'Adidas Originals Futbolka',
        'description': '100% paxta futbolka, klassik dizayn, turli ranglar mavjud.',
        'price': Decimal('199000'),
        'old_price': None,
        'category': categories['Kiyim'],
        'rating': 4.3,
        'reviews_count': 180,
        'stock': 50,
        'is_new': False,
    },
    {
        'name': 'Dyson V11 Changyutgich',
        'description': 'Simsiz changyutgich, kuchli batareya, HEPA filtr, turli qo\'shimcha cho\'tkalar.',
        'price': Decimal('4599000'),
        'old_price': Decimal('5299000'),
        'category': categories['Uy-ro\'zg\'or'],
        'rating': 4.7,
        'reviews_count': 320,
        'stock': 12,
        'is_new': False,
    },
    {
        'name': 'Sony WH-1000XM5 Quloqchin',
        'description': 'Premium shovqinni bekor qiluvchi quloqchin, 30 soat batareya, yuqori sifatli ovoz.',
        'price': Decimal('3299000'),
        'old_price': None,
        'category': categories['Elektronika'],
        'rating': 4.9,
        'reviews_count': 890,
        'stock': 20,
        'is_new': True,
    },
    {
        'name': 'Philips Airfryer XXL',
        'description': 'Katta hajmli havo fritözü, sog\'lom tayyorlash, oson tozalash.',
        'price': Decimal('1899000'),
        'old_price': Decimal('2299000'),
        'category': categories['Uy-ro\'zg\'or'],
        'rating': 4.5,
        'reviews_count': 560,
        'stock': 18,
        'is_new': False,
    },
    {
        'name': 'L\'Oreal Paris Yuz Kremi',
        'description': 'Kundalik parvarish uchun yuz kremi, barcha teri turlari uchun mos.',
        'price': Decimal('149000'),
        'old_price': None,
        'category': categories['Go\'zallik va salomatlik'],
        'rating': 4.2,
        'reviews_count': 95,
        'stock': 100,
        'is_new': False,
    },
]

print("\nCreating products...")
for prod_data in products_data:
    prod, created = Product.objects.get_or_create(
        name=prod_data['name'],
        defaults=prod_data
    )
    print(f"  {'Created' if created else 'Found'}: {prod.name}")

print("\nData population complete!")
print(f"Total categories: {Category.objects.count()}")
print(f"Total products: {Product.objects.count()}")
