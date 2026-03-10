import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from market.models import Product, Category

def assign_categories():
    categories_map = {
        'Shirinliklar': [
            'Chocolate', 'Cookie', 'Wafer', 'Cake', 'Pie', 'Biscuit', 'Marmalade', 'Candy', 
            'Halva', 'Croissant', 'Brownie', 'Oreo', 'Choco', 'Sweet', 'Desert', 'Keks', 
            'Vafli', 'Pechenye', 'Shokolad', 'Konfet', 'Kinder', 'Roshen', 'Yashkino', 'Konti',
            'Alenka', 'Millennium', 'Pobeda', 'Korzinka', 'Rulet', 'Zefir', 'Muffin', 'Waffles',
            'Bounty', 'Snickers', 'Mars', 'Twix', 'KitKat', 'Milka', 'Nestle', 'Nutella'
        ],
        'Snacklar': [
            'Chips', 'Crisps', 'Grenki', 'Nuts', 'Peanuts', 'Pistachio', 'Sunflower', 
            'Pumpkin', 'Seeds', 'Crackers', 'Popcorn', 'Kurt', 'Pretzel', 'Khrus', 
            'Flint', 'Cheers', 'Big Bob', 'Grand', 'Pistachios', 'Almonds', 'Cashews',
            'Lays', 'Pringles', 'Doritos', 'Cheetos', 'Tuc', 'Hrusteam', 'Kruton'
        ],
        'Ichimliklar': [
            'Tea', 'Coffee', 'Juice', 'Water', 'Cola', 'Fanta', 'Sprite', 'Pepsi', 
            'Drink', 'Beverage', 'Choy', 'Kofe', 'Sok', 'Suv', 'Lipton', 'Fuse', 'Dena',
            'Bliss', 'Coca', 'Nestle Water', 'Sharbat', 'Limonad', 'Soda', 'Energy', 
            'Mojito', 'Kompot', 'Viko', 'Agusha', 'Zuegg', 'Flash', 'Gorilla', 'Red Bull',
            'Lemonade', 'Seltzer', 'Rootz', 'Polar'
        ],
        'Sut Mahsulotlari': [
            'Milk', 'Yogurt', 'Kefir', 'Moloko', 'Sut', 'Qatiq', 'Kaymoq', 'Smetana', 
            'Cheese', 'Sir', 'Brinza', 'Tvorog', 'Curd', 'Butter', 'Saryog', 'Maslo'
        ],
        'Tez Tayyorlanadigan': [
            'Ramen', 'Noodle', 'Rolton', 'Big Bon', 'Soup', 'Pyure', 'Puree', 'Cup', 
            'Hot Chicken', 'Buldak', 'Samyang', 'Ottogi', 'Nongshim', 'Shin Ramyun',
            'Fusian', 'K-Quick', 'Yeul Ramen'
        ],
        'Bakaleya': [
            'Macaroni', 'Pasta', 'Spaghetti', 'Oatmeal', 'Oats', 'Oil', 'Rice', 
            'Buckwheat', 'Sugar', 'Salt', 'Flour', 'Makaron', 'Un', 'Yog', 'Guruch', 
            'Grechka', 'Hercules', 'Makiz', 'Makfa', 'Rice'
        ],
        'Bolalar Uchun': [
            'Agusha', 'Honey Kid', 'Malenkoe Schaste', 'Gerber', 'Fruto', 'Baby', 
            'Bolalar', 'Kasha', 'Pyuresi'
        ],
        'Saqichlar': [
            'Gum', 'Orbit', 'Dirol', 'Mentos', 'Eclipse', 'Saqich', 'Chupa Chups', 'Big Babol'
        ],
        'Maishiy Kimyo': [
            'Grass', 'Fairy', 'Tide', 'Lenor', 'Cif', 'Sanita', 'Barf', 'Silver', 
            'Palmolive', 'Dove', 'Arko', 'Soap', 'Shampoo', 'Gel', 'Spray', 'Powder', 
            'Tissue', 'Foam', 'Clean', 'Wash', 'Ariel', 'Persil', 'Vanish', 'Domestos'
        ],
        'Konservalar': [
            'Olives', 'Sauce', 'Fish', 'Meat', 'Canned', 'Jar', 'Vinegar', 'Mustard', 
            'Ketchup', 'Bonduelle', 'Heinz', 'Sen Soy', 'Kaija', 'Banga', 'Foodmaxx', 
            'Amoy', 'Mackerel', 'Salmon', 'Sardine', 'Tuna'
        ]
    }

    # Ensure categories exist
    category_objs = {}
    for cat_name in categories_map.keys():
        category_objs[cat_name], created = Category.objects.get_or_create(name=cat_name)
        if created:
            print(f"Created category: {cat_name}")

    products = Product.objects.all()
    count = 0
    assigned_count = 0
    
    for product in products:
        # Skip if name looks like a timestamp (unnamed)
        if len(product.name) == 19 and product.name[4] == '-' and product.name[7] == '-':
             # Try to match anyway, but likely won't
             pass

        assigned = False
        for cat_name, keywords in categories_map.items():
            for keyword in keywords:
                if keyword.lower() in product.name.lower():
                    product.category = category_objs[cat_name]
                    product.save()
                    print(f"Assigned '{product.name}' to '{cat_name}'")
                    assigned = True
                    assigned_count += 1
                    break
            if assigned:
                break
        
        if not assigned:
            # Check if it has a category already
            if product.category:
                 print(f"Skipped '{product.name}' (already has category {product.category.name}, no new keyword match)")
            else:
                 print(f"Skipped '{product.name}' (no match)")
        count += 1

    print(f"Total products checked: {count}")
    print(f"Total products updated: {assigned_count}")

if __name__ == "__main__":
    assign_categories()
