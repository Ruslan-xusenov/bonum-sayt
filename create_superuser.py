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

print("\n✅ Superuser created successfully!")
print("=" * 50)
print("Username: admin")
print("Password: admin123")
print("=" * 50)
print("\nYou can now login at: http://127.0.0.1:8000/admin/")
