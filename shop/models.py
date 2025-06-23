from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User     

class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_buyer = models.BooleanField('Is buyer', default=False)
    is_vendor = models.BooleanField('Is vendor', default=False)
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

class BuyerInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

class VendorInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    business_location = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username



class Product(models.Model):
    LAPTOP_BRANDS = [
        ('Apple', 'Apple'),
        ('Dell', 'Dell'),
        ('HP', 'HP'),
        ('Lenovo', 'Lenovo'),
        ('Acer', 'Acer'),
        ('Asus', 'Asus'),
        ('Microsoft', 'Microsoft'),
        ('Samsung', 'Samsung'),
        ('MSI', 'MSI'),
        ('LG', 'LG'),
        ('Razer', 'Razer'),
        ('Huawei', 'Huawei'),
        ('Google', 'Google'),
        ('Sony', 'Sony'),
        ('Toshiba', 'Toshiba'),
        ('Fujitsu', 'Fujitsu'),
        ('Alienware', 'Alienware'),
        ('Gigabyte', 'Gigabyte'),
        ('Other', 'Other'),
    ]

    LAPTOP_CATEGORIES = [
        ('Ultrabook', 'Ultrabook'),
        ('Gaming Laptop', 'Gaming Laptop'),
        ('Business Laptop', 'Business Laptop'),
        ('2-in-1 Laptop', '2-in-1 Laptop'),
        ('Chromebook', 'Chromebook'),
        ('Traditional Laptop', 'Traditional Laptop'),
        ('Budget Laptop', 'Budget Laptop'),
        ('Workstation', 'Workstation'),
        ('Student Laptop', 'Student Laptop'),
        ('Other', 'Other'),
    ]

    brand = models.CharField(max_length=255, choices=LAPTOP_BRANDS)
    category = models.CharField(max_length=255, choices=LAPTOP_CATEGORIES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.ForeignKey(VendorInfo, on_delete=models.CASCADE, null=True, default=None)   
    image = models.ImageField(upload_to='product_images/')
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.brand



class Order(models.Model):
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    CANCELLED = 'Cancelled'


    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SHIPPED, 'Shipped'),
        (CANCELLED, 'Cancelled'),
        (PROCESSING, 'Processing'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField(Product, through='OrderItem')
    invoice_number = models.CharField(max_length=100, unique=True, null=True)

    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)


    def __str__(self):
        return f"{self.quantity} of {self.product.brand} in Order {self.order.id}"
    


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def total_price(self):
        return self.quantity * self.product.price
 
   