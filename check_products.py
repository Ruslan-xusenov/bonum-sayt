import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from market.models import Product

total = Product.objects.count()
with_images = Product.objects.exclude(image='').count()

print(f'Jami tovarlar: {total}')
print(f'Rasmli tovarlar: {with_images}')
print(f'Rasmsiz tovarlar: {total - with_images}')
