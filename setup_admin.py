import os
import sys

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.contrib.auth.models import User

# Delete existing admin if exists
if User.objects.filter(username='admin').exists():
    User.objects.filter(username='admin').delete()
    print("Deleted existing admin user")

# Create new superuser
user = User.objects.create_superuser(
    username='admin',
    email='admin@uzummarket.uz',
    password='admin123'
)

print("\n" + "="*60)
print("✅ ADMIN USER CREATED SUCCESSFULLY!")
print("="*60)
print("\nLogin credentials:")
print("  Username: admin")
print("  Password: admin123")
print("\nAdmin panel URL:")
print("  http://127.0.0.1:8000/admin/")
print("="*60)
