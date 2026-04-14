from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    size = models.FloatField()
    price = models.FloatField(default=0)
    discount = models.IntegerField(default=0)
    discount_price = models.FloatField(default=0)
    image = models.ImageField(upload_to='products/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.discount > 0:
            self.discount_price = self.price - self.price * self.discount / 100
        else:
            self.discount_price = self.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        related_name="cart_user",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="cart_product",
        blank=True,
        null=True,
    )
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cart} - {self.product} - {self.quantity}"


class Order(models.Model):
    STATUS_CHOICES = (
        ("new", "New"),
        ("accepted", "Accepted"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        related_name="order_user",
    )
    address = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    delivery_time = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    total_discount = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="order_product",
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.order} - {self.product} - {self.quantity}"

    def save(self, *args, **kwargs):
        if self.product and self.price == 0:
            self.price = self.product.discount_price
        super().save(*args, **kwargs)

    @property
    def subtotal(self):
        return self.price * self.quantity
