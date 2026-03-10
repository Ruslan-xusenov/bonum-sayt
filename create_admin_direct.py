import sqlite3
import hashlib

# Connect to database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Delete existing admin user if exists
cursor.execute("DELETE FROM auth_user WHERE username = 'admin'")

# Django password hash for 'admin123'
# Using PBKDF2 algorithm (Django default)
password = 'pbkdf2_sha256$600000$salt123456789$' + hashlib.pbkdf2_hmac(
    'sha256',
    b'admin123',
    b'salt123456789',
    600000
).hex()

# Insert admin user
cursor.execute("""
    INSERT INTO auth_user (
        username, first_name, last_name, email, password,
        is_superuser, is_staff, is_active, date_joined
    ) VALUES (
        'admin', '', '', 'admin@uzummarket.uz', ?,
        1, 1, 1, datetime('now')
    )
""", (password,))

conn.commit()
conn.close()

print("\n" + "="*60)
print("✅ ADMIN USER CREATED SUCCESSFULLY!")
print("="*60)
print("\nLogin credentials:")
print("  Username: admin")
print("  Password: admin123")
print("\nAdmin panel URL:")
print("  http://127.0.0.1:8000/admin/")
print("="*60)
