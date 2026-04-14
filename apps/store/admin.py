from django.contrib import admin

from apps.store.models import Product, Cart, CartItem, OrderItem, Order


@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ('name', 'size', 'price', 'discount_price')
    search_fields = ('name',)
    list_filter = ('size', 'price', 'discount_price')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart', 'product', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'status')
    search_fields = ('user',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order', 'product', 'quantity')