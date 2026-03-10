import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from market.models import Banner

# Delete all current banners
Banner.objects.all().delete()

# Create new banners
banners = [
    {
        'title': 'NextMarket - Sifatli xizmat',
        'subtitle': 'Barchasi bir yerda!',
        'image': 'banners/banner1.png',
        'order': 1
    },
    {
        'title': 'Keng tanlov',
        'subtitle': 'Eng yangi mahsulotlar',
        'image': 'banners/banner2.png',
        'order': 2
    },
    {
        'title': 'Hordiq va qulaylik',
        'subtitle': 'Istalgan vaqtda buyurtma bering',
        'image': 'banners/banner3.png',
        'order': 3
    }
]

for b_data in banners:
    Banner.objects.create(**b_data)

print("Banners updated successfully!")
