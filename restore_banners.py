import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from market.models import Banner
from django.core.files import File

# Delete existing banners
Banner.objects.all().delete()
print("Deleted all existing banners.")

banners_data = [
    {
        'title': 'Yangi texnologiyalar olami',
        'subtitle': "Eng so'nggi noutbuklar va gadjetlar hamyonbop narxlarda.",
        'image_path': 'static/images/banner1.png',
        'order': 1
    },
    {
        'title': 'Zamonaviy uslub va moda',
        'subtitle': 'Yozgi kolleksiya allaqachon sotuvda. 50% gacha chegirmalar.',
        'image_path': 'static/images/banner2.png',
        'order': 2
    },
    {
        'title': 'Uyingiz uchun qulaylik',
        'subtitle': 'Maishiy texnika dunyosidagi eng yaxshi takliflar faqat bizda.',
        'image_path': 'static/images/banner3.png',
        'order': 3
    }
]

print("Restoring original banners...")
for data in banners_data:
    if os.path.exists(data['image_path']):
        with open(data['image_path'], 'rb') as f:
            banner = Banner.objects.create(
                title=data['title'],
                subtitle=data['subtitle'],
                order=data['order'],
                is_active=True
            )
            banner.image.save(os.path.basename(data['image_path']), File(f), save=True)
            print(f"  Created: {banner.title}")
    else:
        print(f"  Warning: Image not found at {data['image_path']}")

print("Banner restoration complete!")
