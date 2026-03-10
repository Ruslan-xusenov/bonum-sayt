import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from market.models import Category

def add_category():
    category, created = Category.objects.get_or_create(name='Barchasi')
    if created:
        print("Created category: Barchasi")
    else:
        print("Category 'Barchasi' already exists")

if __name__ == '__main__':
    add_category()
