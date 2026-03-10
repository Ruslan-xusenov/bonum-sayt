from market.models import Product
import os
import django

# Set up Django environment if running as a standalone script
# (Though we'll run this via manage.py shell)

def update_products():
    updates = {
        '2026-01-14 15-57-53': 'Khrus Team Baguette',
        '2026-01-14 15-57-09': 'Khrus Team Croutons Shashlik',
        '2026-01-14 15-56-13': 'Flint Grenki Garlic',
        '2026-01-14 15-54-11': 'Dropz Strawberry & Banana',
        '2026-01-14 15-58-51': 'Big Bob Peanuts',
        '2026-01-14 14-12-55': 'Pumpkin Seeds', # Identification based on "Косточки"
    }
    
    for old_name, new_name in updates.items():
        count = Product.objects.filter(name=old_name).update(name=new_name)
        if count:
            print(f"Updated '{old_name}' to '{new_name}'")
        else:
            print(f"Product '{old_name}' not found.")

if __name__ == "__main__":
    update_products()
