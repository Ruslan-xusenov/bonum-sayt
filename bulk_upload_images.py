import os
import django
import shutil
import random
from decimal import Decimal

# Set up environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from market.models import Product, Category

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
PHOTO_DIR = BASE_DIR / 'nextphoto'
MEDIA_DIR = BASE_DIR / 'media' / 'products'

# Ensure media directory exists
os.makedirs(MEDIA_DIR, exist_ok=True)

# Get Barchasi category
try:
    category, created = Category.objects.get_or_create(name='Barchasi')
except Exception as e:
    print(f"Error getting/creating category: {e}")
    exit()

print(f"Using category: {category.name}")
print(f"Processing images from: {PHOTO_DIR}")

# Process images
print(f"Scanning directory: {PHOTO_DIR}")
try:
    files = [f for f in os.listdir(PHOTO_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    print(f"Found {len(files)} image files")
except Exception as e:
    print(f"Error listing directory: {e}")
    exit()

total = len(files)
count = 0

for filename in files:
    try:
        # Generate product name from filename
        name = os.path.splitext(filename)[0].replace('photo_', '').replace('_', ' ').title()
        
        # Check if product already exists to avoid duplicates (optional, based on name)
        # For now, we'll just create new ones to match the "all photos" request
        
        # Random price
        price = Decimal(random.randint(10, 500) * 10000)
        
        # Copy file to media
        src_path = os.path.join(PHOTO_DIR, filename)
        dest_path = os.path.join(MEDIA_DIR, filename)
        
        if not os.path.exists(dest_path):
            shutil.copy(src_path, dest_path)
        
        # Create product
        prod = Product.objects.create(
            name=name,
            description="Premium sifatli mahsulot. Kafolat beriladi.",
            price=price,
            category=category,
            image=f'products/{filename}',
            rating=round(random.uniform(4.0, 5.0), 1),
            reviews_count=random.randint(5, 100),
            stock=random.randint(1, 50),
            is_new=True
        )
        
        count += 1
        if count % 10 == 0:
            print(f"  Progress: {count}/{total}")
            
    except Exception as e:
        print(f"  Error processing {filename}: {e}")

print(f"\nSuccess: Added {count} products with images!")
