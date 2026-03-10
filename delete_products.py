import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from market.models import Product

def delete_all_products():
    count = Product.objects.all().count()
    Product.objects.all().delete()
    print(f"Deleted {count} products.")

if __name__ == '__main__':
    delete_all_products()
