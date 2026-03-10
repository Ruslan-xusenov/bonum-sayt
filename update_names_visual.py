import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from market.models import Product

def update_products_visual():
    updates = {
        '2026-01-14 14-22-19': 'Семена Льна 500г',
        '2026-01-14 14-22-58': 'Orion Choco-Pie Orange & Chocochip',
        '2026-01-14 15-01-01': 'Яшкино Печенье со вкусом пломбира 220г',
        '2026-01-14 15-01-40': 'Roshen Wafers Hazelnut',
        '2026-01-14 15-02-09': 'Roshen Wafers Milk',
        '2026-01-14 15-02-40': 'Roshen Wafers Coconut & Almond',
        '2026-01-14 15-03-09': 'Roshen Wafers Sandwich Milk Vanilla',
        '2026-01-14 15-04-15': 'Roshen Wafers Sandwich Choco',
        '2026-01-14 15-04-43': 'Kinder Plum Cake Yogurt alla Greca',
        '2026-01-14 15-06-05': 'Konti Super Kontik Marshmallow',
        '2026-01-14 15-07-04': 'Яшкино Бисквитный Рулет Клубника со сливками',
        '2026-01-14 15-08-36': 'Roshen Lovita Classic Cookies Cocoa',
        '2026-01-14 15-09-35': 'Florida Cookies Dark with Chocolate-Nut Filling',
        '2026-01-14 15-10-18': 'Konti Bonjour Dessert with Orange',
        '2026-01-14 15-10-45': 'Яшкино Jaffa Cake Вишня 137г',
        '2026-01-14 15-11-54': 'Яшкино Jaffa Cake Апельсин 137г',
        '2026-01-14 15-13-09': 'Яшкино Вихарек с апельсиновым вкусом',
        '2026-01-14 15-14-57': 'Аленка Печенье хрустящее с фундуком и шоколадом',
        '2026-01-14 15-16-12': 'Bounty Soft Baked Cookies',
        '2026-01-14 15-16-50': 'Krember Wafer Cubes с банановым вкусом',
        '2026-01-14 15-17-34': 'Millennium Choco Crunch Nuts Milk Chocolate',
        '2026-01-14 15-18-03': 'Яшкино Итальянские мини-круассаны со сливочным кремом 180г',
        '2026-01-14 15-18-43': 'Яшкино Вафли с халвой 200г',
        '2026-01-14 15-19-23': 'Roshen Lovita Jelly Cookies Orange Flavor 420g',
        '2026-01-14 15-20-07': 'Roshen Lovita Jelly Cookies Strawberry Flavor 420g',
        '2026-01-14 15-20-39': "Konti Mummy's Cake with Raspberry & Pistachio 310g",
        '2026-01-14 15-21-56': "Konti Mummy's Cake with Chocolate Flavor 310g",
        '2026-01-14 15-22-55': 'Вафельный пломбир Сливочный',
        '2026-01-14 15-23-47': 'Вафельный пломбир Шоколадный',
        '2026-01-14 15-22-55': 'Вафельный пломбир Сливочный',
        '2026-01-14 15-23-47': 'Вафельный пломбир Шоколадный',
        '2026-01-14 15-24-26': 'Вафельный пломбир Клубничный',
        '2026-01-14 15-25-20': 'Roshen Lovita Blondie Brownie Lemon',
        '2026-01-14 15-25-49': 'Roshen Lovita Blondie Brownie Coconut',
        '2026-01-14 15-26-41': 'Roshen Lovita Soft Brownie Dark Cocoa',
        '2026-01-14 15-29-19': 'Oreo Original',
        '2026-01-14 15-42-48': 'Cheers Green Onion',
        '2026-01-14 15-43-10': 'Cheers Cheese',
        '2026-01-14 15-43-45': 'Cheers Shashlik',
        '2026-01-14 15-46-02': "Lay's Crab",
        '2026-01-14 15-46-33': 'Cheers Sour Cream & Onion',
        '2026-01-14 15-58-51': 'Flint Grenki Plov',
        '2026-01-28 19-06-38': 'Grand Salted Apricot Kernels 500g',
        '2026-01-14 15-05-19': 'Аленка Печенье с какао и глазурью',
        '2026-01-14 15-59-24': 'Flint Grenki Veal and Adjika',
        '2026-01-14 16-00-13': 'Big Bob Peanuts Grill Sausage',
        '2026-01-14 15-53-35': 'Cheers Dropz Orange',
        '2026-01-14 15-51-04': 'Cheers Nachos Cheese',
        '2026-01-14 15-47-45': 'Cheers Nachos Chili Sausage',
        '2026-01-14 15-57-53': 'Khrus Team Baguette Sour Cream & Herbs',
        '2026-01-14 15-57-09': 'Khrus Team Shashlik Croutons',
        '2026-01-14 15-56-13': 'Flint Grenki Garlic',
        '2026-01-14 15-54-11': 'Dropz Strawberry & Banana',
        '2026-01-12 16-44-29': 'LAYS STAX Sour Cream & Onion', # Likely Lays Stax based on common e-commerce items
        '2026-01-12 16-46-10': 'LAYS STAX Original',
        '2026-01-12 16-48-02': 'LAYS STAX Paprika',
    }
    
    for old_name, new_name in updates.items():
        count = Product.objects.filter(name=old_name).update(name=new_name)
        if count:
            print(f"Updated '{old_name}' to '{new_name}'")
        else:
            # Try searching by image name if name was already changed but not finalized
            p = Product.objects.filter(image__contains=old_name.replace(' ', '_').replace('-', '_')).first()
            if p:
                old_actual_name = p.name
                p.name = new_name
                p.save()
                print(f"Updated (via image) '{old_actual_name}' to '{new_name}'")
            else:
                print(f"Product related to '{old_name}' not found.")

if __name__ == "__main__":
    update_products_visual()
