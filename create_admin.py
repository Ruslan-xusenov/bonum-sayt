import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Create admin user
username = 'admin'
email = 'admin@uzummarket.uz'
password = 'admin123'

if User.objects.filter(username=username).exists():
    print(f"User '{username}' already exists!")
    user = User.objects.get(username=username)
    print(f"Username: {username}")
    print(f"Password: {password}")
else:
    user = User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser created successfully!")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"\nYou can now login at: http://127.0.0.1:8000/admin/")
