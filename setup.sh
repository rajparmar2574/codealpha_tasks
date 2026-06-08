#!/bin/bash
# LuxeCart E-commerce Setup Script
echo "🛍️  Setting up LuxeCart E-commerce..."
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install django pillow --break-system-packages -q
echo "✅ Dependencies installed"

# Database setup
echo ""
echo "🗄️  Setting up database..."
python manage.py makemigrations store
python manage.py migrate
echo "✅ Database ready"

# Seed data
echo ""
echo "🌱 Seeding sample products..."
python manage.py seed_data

# Create superuser
echo ""
echo "👤 Creating admin user (admin / admin123)..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@luxecart.com', 'admin123')
    print('✅ Admin created: admin / admin123')
else:
    print('⏭️  Admin already exists')
"

echo ""
echo "======================================"
echo "🎉 LuxeCart is ready!"
echo "======================================"
echo ""
echo "Run the server:"
echo "  python manage.py runserver"
echo ""
echo "Then open: http://127.0.0.1:8000"
echo ""
echo "Admin panel: http://127.0.0.1:8000/admin"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
