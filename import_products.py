import os
import sys
import django

# Setup Django
sys.path.append(r'C:\Users\User\Desktop\next-sayt')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nextmarket.settings')
django.setup()

import random
from market.models import Product, Category
from django.core.files import File

# Get or create Barchasi category
barchasi, created = Category.objects.get_or_create(name='Barchasi')
print(f"Barchasi toifasi: {'yaratildi' if created else 'mavjud'}")

# Path to images
image_dir = r'C:\Users\User\Desktop\nextphoto'
if not os.path.exists(image_dir):
    print(f"Xatolik: {image_dir} papka topilmadi!")
    sys.exit(1)

image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
print(f"Topilgan rasmlar: {len(image_files)}")

# Create products
count = 0
for i, img_file in enumerate(image_files[:100], 1):
    img_path = os.path.join(image_dir, img_file)
    
    try:
        with open(img_path, 'rb') as f:
            product = Product.objects.create(
                name=f"Mahsulot {i}",
                description=f"Bu {i}-mahsulot haqida batafsil ma'lumot. Yuqori sifatli va ishonchli mahsulot.",
                price=random.randint(50000, 500000),
                old_price=random.randint(600000, 800000),
                category=barchasi,
                stock=random.randint(5, 50)
            )
            product.image.save(img_file, File(f), save=True)
            count += 1
        
        if i % 20 == 0:
            print(f"{i} ta mahsulot qo'shildi...")
    except Exception as e:
        print(f"Xatolik {img_file}: {e}")

print(f"\n✅ Jami {count} ta mahsulot muvaffaqiyatli qo'shildi!")
print(f"Bazadagi jami mahsulotlar: {Product.objects.count()}")
