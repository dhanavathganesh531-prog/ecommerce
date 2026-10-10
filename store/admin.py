from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_price', 'stock', 'is_available', 'is_featured', 'created_at']
    list_filter = ['category', 'is_available', 'is_featured']
    list_editable = ['price', 'discount_price', 'stock', 'is_available', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    raw_id_fields = ['product']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'created_at', 'updated_at']
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'product_name', 'price', 'quantity', 'get_total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = "Total"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'phone', 'total_amount', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['id', 'full_name', 'email', 'phone', 'address']
    list_editable = ['status']
    inlines = [OrderItemInline]
