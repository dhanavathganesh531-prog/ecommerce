from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from store.models import Category, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seed the database with sample categories, products, and a demo admin user'

    def handle(self, *args, **options):
        self.stdout.write("Starting database seeding...")

        # 1. Create Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin / admin123'))
        else:
            self.stdout.write('Superuser already exists.')

        # 2. Categories
        categories_data = [
            {'name': 'Audio & Headphones', 'description': 'Immersive sound engineering, wireless earbuds, and studio monitors.'},
            {'name': 'Smart Tech & Wearables', 'description': 'Cutting edge smartwatches, trackers, and intelligent accessories.'},
            {'name': 'Apparel & Footwear', 'description': 'Ergonomic, modern streetwear and athletic performance shoes.'},
            {'name': 'Everyday Carry', 'description': 'Minimalist wallets, durable backpacks, and modern lifestyle essentials.'},
        ]

        category_objs = {}
        for cat in categories_data:
            obj, _ = Category.objects.get_or_create(
                slug=slugify(cat['name']),
                defaults={'name': cat['name'], 'description': cat['description']}
            )
            category_objs[cat['name']] = obj

        # 3. Products
        products_data = [
            {
                'category': category_objs['Audio & Headphones'],
                'name': 'Aura Studio Wireless Noise-Cancelling Headphones',
                'description': 'Experience true acoustic precision with custom 40mm beryllium drivers, 38-hour battery longevity, and dual-mode hybrid active noise cancellation.',
                'price': Decimal('299.99'),
                'discount_price': Decimal('249.99'),
                'stock': 24,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80',
                'is_featured': True,
            },
            {
                'category': category_objs['Audio & Headphones'],
                'name': 'EchoPulse True Wireless Earbuds',
                'description': 'Compact waterproof IPX7 earbuds with ultra-low latency gaming mode, ambient transparency, and Qi wireless charging case.',
                'price': Decimal('119.50'),
                'discount_price': Decimal('89.00'),
                'stock': 40,
                'image_url': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&auto=format&fit=crop&q=80',
                'is_featured': True,
            },
            {
                'category': category_objs['Smart Tech & Wearables'],
                'name': 'Vanguard Chrono Smartwatch Series 6',
                'description': 'Aerospace-grade titanium casing, sapphire crystal display, ECG heart monitoring, altitude sensors, and seamless cellular connectivity.',
                'price': Decimal('349.00'),
                'discount_price': None,
                'stock': 15,
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80',
                'is_featured': True,
            },
            {
                'category': category_objs['Smart Tech & Wearables'],
                'name': 'FitPulse Band Pro 3',
                'description': 'Ultra-lightweight fitness tracker with AMOLED touch display, continuous SpO2 monitoring, and 14-day battery life.',
                'price': Decimal('69.99'),
                'discount_price': Decimal('54.99'),
                'stock': 50,
                'image_url': 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=800&auto=format&fit=crop&q=80',
                'is_featured': False,
            },
            {
                'category': category_objs['Apparel & Footwear'],
                'name': 'Aerorun Breathable Performance Sneakers',
                'description': 'Engineered knit upper with responsive energy-return foam cushioning for effortless marathon running and all-day city walks.',
                'price': Decimal('139.00'),
                'discount_price': Decimal('115.00'),
                'stock': 18,
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&auto=format&fit=crop&q=80',
                'is_featured': True,
            },
            {
                'category': category_objs['Apparel & Footwear'],
                'name': 'Urban Minimalist Heavyweight Hoodie',
                'description': 'Crafted from 100% organic French terry cotton with relaxed tailored drape, reinforced seams, and double-lined hood.',
                'price': Decimal('85.00'),
                'discount_price': None,
                'stock': 35,
                'image_url': 'https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=800&auto=format&fit=crop&q=80',
                'is_featured': False,
            },
            {
                'category': category_objs['Everyday Carry'],
                'name': 'Nomad Weatherproof Travel Backpack 28L',
                'description': 'Constructed from ballistic Cordura nylon featuring dedicated 16-inch fleece laptop sleeve, hidden passport pocket, and magnetic buckles.',
                'price': Decimal('179.00'),
                'discount_price': Decimal('149.00'),
                'stock': 20,
                'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&auto=format&fit=crop&q=80',
                'is_featured': True,
            },
            {
                'category': category_objs['Everyday Carry'],
                'name': 'Slim Carbon Fiber RFID Blocking Wallet',
                'description': 'Holds up to 12 cards with elastic expansion band, money clip, and military-grade RFID protection against electronic theft.',
                'price': Decimal('49.99'),
                'discount_price': Decimal('39.99'),
                'stock': 60,
                'image_url': 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=800&auto=format&fit=crop&q=80',
                'is_featured': False,
            },
        ]

        for p in products_data:
            slug = slugify(p['name'])
            product, created = Product.objects.get_or_create(
                slug=slug,
                defaults=p
            )
            if created:
                self.stdout.write(f"Added product: {product.name}")

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with demo categories and products!"))
