import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from market.models import Product

import json

def list_products_needing_names():
    # Products with names that look like timestamps
    products = Product.objects.all()
    needing_names = []
    for p in products:
        # Check if name follows the pattern YYYY-MM-DD HH-MM-SS
        if len(p.name) == 19 and p.name[4] == '-' and p.name[10] == ' ':
            needing_names.append({
                'id': p.id,
                'current_name': p.name,
                'image_path': p.image.path if p.image else None,
                'image_url': p.image.url if p.image else None
            })
    
    print(f"Found {len(needing_names)} products needing names.")
    
    with open('products_to_process.json', 'w') as f:
        json.dump(needing_names, f, indent=2)
    print("Saved to products_to_process.json")

if __name__ == "__main__":
    list_products_needing_names()
