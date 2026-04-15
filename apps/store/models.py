from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(max_length=255)
    volume = models.CharField(max_length=50)
    price = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name

    @property
    def active_promotion(self):
        return self.promotions.filter(is_active=True).order_by("-id").first()

    @property
    def discount_percent(self):
        promo = self.active_promotion
        return promo.discount_percent if promo else 0

    @property
    def final_price(self):
        promo = self.active_promotion
        if promo and promo.discount_percent > 0:
            return self.price - (self.price * promo.discount_percent // 100)
        return self.price


class Promotion(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="promotions",
    )
    discount_percent = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        "users.TelegramUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_promotions",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.product} - {self.discount_percent}%"

    def save(self, *args, **kwargs):
        if self.is_active:
            Promotion.objects.filter(product=self.product, is_active=True).exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.OneToOneField(
        "users.TelegramUser",
        on_delete=models.CASCADE,
        related_name="cart",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Cart - {self.user}"

    @property
    def subtotal(self):
        return sum(item.product.price * item.quantity for item in self.items.select_related("product"))

    @property
    def discount_amount(self):
        return sum((item.product.price - item.product.final_price) * item.quantity for item in self.items.select_related("product"))

    @property
    def total_amount(self):
        return sum(item.product.final_price * item.quantity for item in self.items.select_related("product"))


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("cart", "product")
        ordering = ["id"]

    def __str__(self):
        return f"{self.cart} - {self.product} - {self.quantity}"

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    @property
    def total_price(self):
        return self.product.final_price * self.quantity

    @property
    def discount_amount(self):
        return (self.product.price - self.product.final_price) * self.quantity


class Order(models.Model):
    STATUS_CHOICES = (
        ("new", "New"),
        ("accepted", "Accepted"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(
        "users.TelegramUser",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    phone = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    delivery_time = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    subtotal = models.PositiveIntegerField(default=0)
    discount_amount = models.PositiveIntegerField(default=0)
    total_amount = models.PositiveIntegerField(default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"Order #{self.id} - {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items",
    )
    quantity = models.PositiveIntegerField(default=1)

    unit_price = models.PositiveIntegerField(default=0)
    discount_percent = models.PositiveIntegerField(default=0)
    discount_amount = models.PositiveIntegerField(default=0)
    final_price = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.order} - {self.product} - {self.quantity}"

    def save(self, *args, **kwargs):
        if self.product and self.unit_price == 0:
            self.unit_price = self.product.price
            self.discount_percent = self.product.discount_percent
            self.final_price = self.product.final_price
            self.discount_amount = self.unit_price - self.final_price
        super().save(*args, **kwargs)

    @property
    def subtotal(self):
        return self.final_price * self.quantity


class BotSetting(models.Model):
    operator_telegram_id = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return f"Operator ID: {self.operator_telegram_id}"



class Feedback(models.Model):
    class RatingChoices(models.TextChoices):
        FIVE_STARS = "5", _("⭐⭐⭐⭐⭐")
        FOUR_STARS = "4", _("⭐⭐⭐⭐")
        THREE_STARS = "3", _("⭐⭐⭐")
        TWO_STARS = "2", _("⭐⭐")
        ONE_STAR = "1", _("⭐")

    user = models.ForeignKey(
        "users.TelegramUser",
        on_delete=models.CASCADE,
        related_name="feedbacks",
    )
    rating = models.CharField(
        max_length=1,
        choices=RatingChoices.choices,
        default=RatingChoices.FIVE_STARS,
    )
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.user} - {self.get_rating_display()}"


