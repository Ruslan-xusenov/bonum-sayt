import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from market.models import Category

try:
    c = Category.objects.get(pk=2)
    print(f"ID: {c.id}, Name: {c.name}, Parent: {c.parent}")
    
    # Check if there are other categories
    print("\nAll Categories:")
    for cat in Category.objects.all():
        print(f"- {cat.id}: {cat.name}")

except Exception as e:
    print(f"Error: {e}")