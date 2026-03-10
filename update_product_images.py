import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from market.models import Product

# Image mapping (from artifacts to products)
image_mapping = {
    'iPhone 15 Pro': 'C:/Users/sensorika/.gemini/antigravity/brain/45c8578c-345d-4857-8ad9-4d60f7120bfa/iphone_15_pro_1770116757348.png',
    'Samsung Galaxy S24': 'C:/Users/sensorika/.gemini/antigravity/brain/45c8578c-345d-4857-8ad9-4d60f7120bfa/samsung_galaxy_s24_1770116772958.png',
    'MacBook Pro': 'C:/Users/sensorika/.gemini/antigravity/brain/45c8578c-345d-4857-8ad9-4d60f7120bfa/macbook_pro_1770116786725.png',
    'Samsung TV': 'C:/Users/sensorika/.gemini/antigravity/brain/45c8578c-345d-4857-8ad9-4d60f7120bfa/samsung_tv_1770116813970.png',
    'Zara Kurtka': 'C:/Users/sensorika/.gemini/antigravity/brain/45c8578c-345d-4857-8ad9-4d60f7120bfa/zara_jacket_1770116826848.png',
    'Puma Kostyum': 'C:/Users/sensorika/.gemini/antigravity/brain/45c8578c-345d-4857-8ad9-4d60f7120bfa/puma_tracksuit_1770116839966.png',
}

# Create media/products directory if it doesn't exist
products_dir = 'media/products'
os.makedirs(products_dir, exist_ok=True)

# Copy images to media folder and update products
for product_name, image_path in image_mapping.items():
    try:
        products = Product.objects.filter(name__icontains=product_name.split()[0])
        if products.exists():
            product = products.first()
            
            # Copy image to media folder
            filename = os.path.basename(image_path)
            dest_path = os.path.join(products_dir, filename)
            
            if os.path.exists(image_path):
                shutil.copy(image_path, dest_path)
                
                # Update product image field
                product.image = f'products/{filename}'
                product.save()
                
                print(f'✅ Updated: {product.name} -> {filename}')
            else:
                print(f'❌ Image not found: {image_path}')
        else:
            print(f'⚠️  Product not found: {product_name}')
    except Exception as e:
        print(f'❌ Error updating {product_name}: {e}')

print('\n' + '='*60)
print('Image update complete!')
print('='*60)
