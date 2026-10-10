from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from decimal import Decimal


class EcommerceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Laptop',
            slug='test-laptop',
            description='A high-performance test laptop.',
            price=Decimal('999.99'),
            stock=10,
            is_available=True,
            is_featured=True,
        )

    def test_home_page_status(self):
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Laptop')

    def test_products_list_status(self):
        response = self.client.get(reverse('store:products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Laptop')

    def test_product_detail_status(self):
        response = self.client.get(reverse('store:product_detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Laptop')

    def test_add_to_cart_and_view_cart(self):
        response = self.client.post(
            reverse('store:add_to_cart', args=[self.product.id]),
            {'quantity': 2},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        cart = Cart.objects.first()
        self.assertIsNotNone(cart)
        self.assertEqual(cart.get_total_items(), 2)

    def test_checkout_submission(self):
        # Add item to cart first
        self.client.post(reverse('store:add_to_cart', args=[self.product.id]), {'quantity': 1})

        # Submit checkout form
        checkout_data = {
            'full_name': 'Alice Smith',
            'email': 'alice@example.com',
            'phone': '1234567890',
            'address': '123 Main Street',
            'city': 'Metropolis',
            'postal_code': '10001',
            'payment_method': 'cod',
        }
        response = self.client.post(reverse('store:checkout'), checkout_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check Order was created
        order = Order.objects.filter(email='alice@example.com').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product, self.product)
