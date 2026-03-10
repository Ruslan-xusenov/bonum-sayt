import sqlite3
from hashlib import pbkdf2_hmac
import base64

# Connect to database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Delete existing admin user
cursor.execute("DELETE FROM auth_user WHERE username = 'admin'")

# Create proper Django password hash
salt = 'randomsalt12345'
password = 'admin123'
iterations = 600000

# Generate hash
hash_bytes = pbkdf2_hmac('sha256', password.encode(), salt.encode(), iterations)
hash_b64 = base64.b64encode(hash_bytes).decode('ascii').strip()

# Django password format: algorithm$iterations$salt$hash
django_password = f'pbkdf2_sha256${iterations}${salt}${hash_b64}'

# Insert admin user
cursor.execute("""
    INSERT INTO auth_user (
        id, username, first_name, last_name, email, password,
        is_superuser, is_staff, is_active, date_joined
    ) VALUES (
        1, 'admin', 'Admin', 'User', 'admin@uzummarket.uz', ?,
        1, 1, 1, datetime('now')
    )
""", (django_password,))

conn.commit()
conn.close()

print("\n" + "="*60)
print("✅ ADMIN USER CREATED!")
print("="*60)
print("\nCredentials:")
print("  Username: admin")
print("  Password: admin123")
print("\nURL: http://127.0.0.1:8000/admin/")
print("="*60)
