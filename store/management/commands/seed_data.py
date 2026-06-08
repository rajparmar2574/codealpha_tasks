from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Category, Product


CATEGORIES = [
    {'name': 'Electronics', 'slug': 'electronics', 'icon': '⚡'},
    {'name': 'Fashion', 'slug': 'fashion', 'icon': '👗'},
    {'name': 'Home & Kitchen', 'slug': 'home-kitchen', 'icon': '🏠'},
    {'name': 'Books', 'slug': 'books', 'icon': '📚'},
    {'name': 'Sports', 'slug': 'sports', 'icon': '🏃'},
    {'name': 'Beauty', 'slug': 'beauty', 'icon': '✨'},
]

PRODUCTS = [
    {
        'name': 'Premium Wireless Headphones',
        'category': 'electronics',
        'description': 'Experience crystal-clear audio with our premium noise-cancelling wireless headphones. Features 30-hour battery life, premium drivers, and ultra-comfortable ear cushions. Perfect for music lovers and professionals alike.',
        'price': 2999, 'original_price': 4999, 'stock': 50,
        'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600',
        'rating': 4.8, 'review_count': 234, 'is_featured': True,
    },
    {
        'name': 'Smart Watch Pro X',
        'category': 'electronics',
        'description': 'Advanced smartwatch with health tracking, GPS, and a stunning AMOLED display. Monitor your heart rate, sleep, steps, and calories. Water resistant up to 50 meters.',
        'price': 8999, 'original_price': 12999, 'stock': 30,
        'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600',
        'rating': 4.7, 'review_count': 189, 'is_featured': True,
    },
    {
        'name': 'Mechanical Gaming Keyboard',
        'category': 'electronics',
        'description': 'RGB backlit mechanical keyboard with tactile switches. Ideal for gaming and typing with anti-ghosting technology and durable aluminum frame.',
        'price': 3499, 'original_price': None, 'stock': 40,
        'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600',
        'rating': 4.6, 'review_count': 143, 'is_featured': False,
    },
    {
        'name': 'Designer Leather Jacket',
        'category': 'fashion',
        'description': 'Crafted from genuine Italian leather, this jacket combines timeless style with modern cuts. Features satin lining, YKK zippers, and reinforced stitching for durability.',
        'price': 5499, 'original_price': 7999, 'stock': 20,
        'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600',
        'rating': 4.9, 'review_count': 98, 'is_featured': True,
    },
    {
        'name': 'Classic White Sneakers',
        'category': 'fashion',
        'description': 'Minimalist white sneakers with premium canvas upper and cushioned insole. Versatile design pairs with any outfit, from casual to semi-formal.',
        'price': 1799, 'original_price': 2499, 'stock': 75,
        'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600',
        'rating': 4.5, 'review_count': 312, 'is_featured': True,
    },
    {
        'name': 'Linen Summer Shirt',
        'category': 'fashion',
        'description': 'Breathable 100% linen shirt perfect for warm weather. Available in multiple colors with a relaxed fit that keeps you cool and stylish.',
        'price': 899, 'original_price': None, 'stock': 60,
        'image_url': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600',
        'rating': 4.3, 'review_count': 87, 'is_featured': False,
    },
    {
        'name': 'Non-stick Cookware Set',
        'category': 'home-kitchen',
        'description': 'Complete 8-piece cookware set with premium non-stick coating. Dishwasher safe, oven safe up to 180°C. Perfect for healthy cooking with less oil.',
        'price': 2299, 'original_price': 3499, 'stock': 25,
        'image_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600',
        'rating': 4.7, 'review_count': 156, 'is_featured': False,
    },
    {
        'name': 'Automatic Coffee Maker',
        'category': 'home-kitchen',
        'description': 'Brew barista-quality coffee at home with this programmable 12-cup coffee maker. Features thermal carafe to keep coffee hot for hours.',
        'price': 4499, 'original_price': 5999, 'stock': 18,
        'image_url': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600',
        'rating': 4.8, 'review_count': 203, 'is_featured': True,
    },
    {
        'name': 'Atomic Habits — James Clear',
        'category': 'books',
        'description': 'The #1 New York Times bestseller. Learn proven strategies for forming good habits, breaking bad ones, and mastering the tiny behaviors that lead to remarkable results.',
        'price': 499, 'original_price': 699, 'stock': 100,
        'image_url': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600',
        'rating': 4.9, 'review_count': 521, 'is_featured': False,
    },
    {
        'name': 'Yoga Mat Pro — 6mm',
        'category': 'sports',
        'description': 'Extra thick 6mm non-slip yoga mat with alignment lines. Eco-friendly TPE material, sweat-resistant surface, and carrying strap included.',
        'price': 1299, 'original_price': 1899, 'stock': 45,
        'image_url': 'https://images.unsplash.com/photo-1592432678016-e910b452f9a2?w=600',
        'rating': 4.6, 'review_count': 178, 'is_featured': False,
    },
    {
        'name': 'Vitamin C Serum',
        'category': 'beauty',
        'description': '20% Vitamin C serum with hyaluronic acid and vitamin E. Brightens skin tone, reduces dark spots, and boosts collagen production for youthful skin.',
        'price': 799, 'original_price': 1199, 'stock': 80,
        'image_url': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=600',
        'rating': 4.7, 'review_count': 267, 'is_featured': True,
    },
    {
        'name': 'Wireless Earbuds TWS',
        'category': 'electronics',
        'description': 'True wireless earbuds with active noise cancellation, 8-hour battery, IPX5 water resistance. Premium sound with bass boost and crystal-clear calls.',
        'price': 1999, 'original_price': 3499, 'stock': 55,
        'image_url': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600',
        'rating': 4.5, 'review_count': 342, 'is_featured': True,
    },
]


class Command(BaseCommand):
    help = 'Seed database with sample products and categories'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding database...')

        cat_map = {}
        for cat_data in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name'], 'icon': cat_data['icon']}
            )
            cat_map[cat_data['slug']] = cat
            self.stdout.write(f'  {"✅ Created" if created else "⏭️ Exists"} category: {cat.name}')

        for prod_data in PRODUCTS:
            cat = cat_map.get(prod_data['category'])
            slug = slugify(prod_data['name'])
            prod, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': prod_data['name'],
                    'category': cat,
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'original_price': prod_data.get('original_price'),
                    'stock': prod_data['stock'],
                    'image_url': prod_data.get('image_url', ''),
                    'rating': prod_data['rating'],
                    'review_count': prod_data['review_count'],
                    'is_featured': prod_data['is_featured'],
                }
            )
            self.stdout.write(f'  {"✅ Created" if created else "⏭️ Exists"} product: {prod.name}')

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('👉 Run: python manage.py runserver'))
