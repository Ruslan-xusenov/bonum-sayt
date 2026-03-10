import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from market.models import Product

def list_products_batch(offset=0, limit=10):
    products = Product.objects.filter(name__regex=r'^\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}$')
    batch = products[offset:offset+limit]
    
    results = []
    for p in batch:
        results.append({
            'id': p.id,
            'name': p.name,
            'image_url': p.image.url if p.image else None,
            'image_path': p.image.path if p.image else None
        })
    
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    import sys
    offset = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    list_products_batch(offset, limit)
