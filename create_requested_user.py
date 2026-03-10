import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

username = 'username'
password = 'password'

if User.objects.filter(username=username).exists():
    User.objects.filter(username=username).delete()
    print(f"Deleted existing user: {username}")

User.objects.create_superuser(
    username=username,
    email='user@example.com',
    password=password
)

print(f"\nSuperuser created successfully!")
print("=" * 50)
print(f"Username: {username}")
print(f"Password: {password}")
print("=" * 50)
