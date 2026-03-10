import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from market.models import Product

def populate_keywords():
    keyword_map = {
        # Sweets
        'chocolate': 'shokolad, shirinlik, plitka, milka, nestle, alpen gold',
        'cookie': 'pechenye, pishiriq, pecheniy, shirinlik',
        'wafer': 'vafli, vafli noni, shirinlik',
        'cake': 'tort, keks, pirog, shirinlik, rulet',
        'candy': 'konfet, shirinlik, karamel, shimildiroq',
        'halva': 'holva, pashmak, shirinlik',
        'croissant': 'kruassan, bulochka, shirinlik',
        'brownie': 'brauni, keks, shokoladli pirog',
        'biscuit': 'biskvit, pechenye',
        'marmalade': 'marmelad, jele',
        
        # Snacks
        'chips': 'chips, kartoshka, qarsildoq, sneck',
        'crisps': 'chips, kartoshka',
        'grenki': 'grenki, suxarik, nonli qarsildoq, qotgan non',
        'nuts': 'yong\'oq, yongoq, mag\'iz, magiz, donak',
        'peanut': 'yer yong\'oq, yer yongoq, pista',
        'pistachio': 'pista, xandon pista, yong\'oq',
        'sunflower': 'kungaboqar, semichka, pista',
        'pumpkin': 'qovoq urug\'i, donak',
        'seeds': 'urug\'lar, donak, pista',
        'cracker': 'kreker, pechenye, sho\'r pechenye',
        'popcorn': 'popkorn, makkajo\'xori',
        'kurt': 'qurt, qurut, sho\'r qurt',
        'pretzel': 'kraker, sho\'r tayoqcha',
        'apricot kernel': 'donak, sho\'r donak, o\'rik donagi, mag\'iz',
        'almond': 'bodom, yong\'oq',
        'cashew': 'keşyu, kesh’yu, yong\'oq',
        
        # Drinks
        'tea': 'choy, ko\'k choy, qora choy, damlama',
        'coffee': 'kofe, qahva, nescafe, maccoffee',
        'juice': 'sok, sharbat, mevali ichimlik',
        'water': 'suv, ichimlik suvi, mineral suv',
        'cola': 'kola, coca cola, gazli suv, ichimlik',
        'pepsi': 'pepsi, gazli suv, ichimlik',
        'fanta': 'fanta, gazli suv, apelsin suvi',
        'sprite': 'sprite, gazli suv, limonli suv',
        'drink': 'ichimlik, suv',
        'beverage': 'ichimlik',
        'lemonade': 'limonad, gazli suv, salqin ichimlik',
        'energy': 'energetik, quvvat beruvchi, flash, gorilla, red bull',
        'mojito': 'moxito, kokteyl, salqin ichimlik',
        'kompot': 'kompot, mevali suv',
        
        # Dairy
        'milk': 'sut, moloko, qaymoqli sut',
        'yogurt': 'yogurt, qatiq, mevali yogurt',
        'kefir': 'kefir, qatiq, ayron',
        'cheese': 'pishloq, sir, brınza',
        'curd': 'tvorog, suzma',
        'butter': 'saryog\', maslo',
        'sour cream': 'smetana, qaymoq',
        
        # Cleaning/Household
        'soap': 'sovun, suyuq sovun, qo\'l yuvish',
        'shampoo': 'shampun, soch yuvish',
        'detergent': 'kir yuvish kukuni, poroshok, gel',
        'dish': 'idish yuvish, gel, fairy',
        'cleaner': 'tozalovchi, tozalash vositasi',
        'spray': 'sprey, sepiladigan vosita',
        'tissue': 'salfetka, qog\'oz',
        'foam': 'ko\'pik, soqol olish ko\'pigi',
        'wash': 'yuvish vositasi',
        'bleach': 'oqartiruvchi, xlor',
        
        # Grocery
        'pasta': 'makaron, xamir ovqat',
        'macaroni': 'makaron, spiral',
        'spaghetti': 'spagit, uzun makaron',
        'oil': 'yog\', o\'simlik yog\'i, kungaboqar yog\'i',
        'rice': 'guruch, palov guruchi, osh',
        'sugar': 'shakar, qand',
        'salt': 'tuz, osh tuzi',
        'flour': 'un, bug\'doy uni',
        'oat': 'suli yormasi, gerkules, kasha',
        
        # Instant Food
        'ramen': 'ramen, koreys lag\'mon, tez tayyorlanadigan',
        'noodle': 'lapsha, tezpishar, rolton',
        'puree': 'pyure, kartoshka pyuresi',
        'soup': 'sho\'rva, tez tayyor sho\'rva',
        
        # Baby
        'baby': 'bolalar ovqati, kasha',
        'kids': 'bolalar uchun',
        
        # Gum
        'gum': 'saqich, jvachka, orbit, dirol',
        
        # Canned
        'olive': 'zaytun, olivki',
        'sauce': 'sous, ketçup, mayonez',
        'fish': 'baliq, saury, sardina',
        'meat': 'go\'sht, tushenka',
        'canned': 'konserva, banka',
    }

    products = Product.objects.all()
    count = 0
    updated_count = 0
    
    print(f"Checking keywords for {products.count()} products...")

    for product in products:
        name_lower = product.name.lower()
        new_keywords = []
        
        for key, value in keyword_map.items():
            if key in name_lower:
                # Avoid adding same keywords multiple times
                keywords_list = value.split(', ')
                for reaction in keywords_list:
                     if reaction not in new_keywords:
                         new_keywords.append(reaction)
        
        if new_keywords:
            # Check existing keywords to avoid overwrite/duplicates if run multiple times
            existing_keywords = product.keywords if product.keywords else ""
            final_keywords = existing_keywords
            
            added_any = False
            for kw in new_keywords:
                if kw not in final_keywords:
                    if final_keywords:
                        final_keywords += ", " + kw
                    else:
                        final_keywords = kw
                    added_any = True
            
            if added_any:
                product.keywords = final_keywords
                product.save()
                print(f"Updated '{product.name}': Added '{', '.join(new_keywords)}'")
                updated_count += 1
        
        count += 1

    print(f"Total products updated with keywords: {updated_count}")

if __name__ == "__main__":
    populate_keywords()
