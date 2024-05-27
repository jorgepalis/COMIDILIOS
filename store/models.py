from django.db import models
from Auth.models import User
from django.utils.text import slugify

# Create your models here.
ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Shop(models.Model):
    user = models.OneToOneField(User, related_name='products', on_delete=models.SET_NULL,
                                blank=True, null=True, limit_choices_to={'is_vendor': True})
    owner_email = models.EmailField(unique=True, blank=True, null=True)
    owner_name = models.CharField(max_length=255, blank=True, default='')
    owner_phone = models.CharField(max_length=255, blank=True, default='')
    address = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='shop_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_discount = models.BooleanField(default=False)
    stars = models.IntegerField(blank=True, null=True)
    reviews = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or Shop.objects.filter(pk=self.pk, name=self.name).exists():
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='subcategory_images/', blank=True, null=True)
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, blank=True, null=True, related_name='main_sub_categories')
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug or SubCategory.objects.filter(pk=self.pk, name=self.name).exists():
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(
        upload_to='category_images/', blank=True, null=True)
    sub_categories = models.ManyToManyField(
        SubCategory, blank=True, related_name='main_categories')

    def __str__(self):
        return f'{self.name}'
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug or Category.objects.filter(pk=self.pk, name=self.name).exists():
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tags(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class AttributeChild(models.Model):
    name = models.CharField(max_length=255)
    # price = models.FloatField(blank=True, null=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class Attribute(models.Model):
    name = models.CharField(max_length=255)
    attribute_child = models.ManyToManyField(AttributeChild, blank=True)

    def __str__(self):
        return f'{self.name}'


class Variation(models.Model):
    # item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, blank=True, null=True)
    child = models.ForeignKey(
        AttributeChild, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.attribute.name} - {self.child.name} - {self.price}'


class Item(models.Model):
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, blank=True, null=True)
    selected_cat_sub_categories_id = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    attributes = models.ManyToManyField(Attribute, blank=True)
    variations = models.ManyToManyField(Variation, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    inventory = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    stars = models.IntegerField(blank=True, null=True)
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ItemAttribute(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.ManyToManyField(AttributeChild, blank=True)

    def __str__(self):
        return f"{self.item} -"

    class Meta:
        unique_together = ('item', 'attribute')


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(
        Shop, on_delete=models.SET_NULL, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    rider = models.ForeignKey(User, related_name='rider', on_delete=models.SET_NULL,
                              blank=True, null=True, limit_choices_to={'is_rider': True})
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'is_client': True})
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, blank=True, null=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Address(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    zip = models.CharField(max_length=100, blank=True, null=True)
    address_type = models.CharField(
        max_length=1, choices=ADDRESS_CHOICES, blank=True, null=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"
