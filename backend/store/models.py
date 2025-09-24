from django.db import models
from . import validators
from django.contrib.auth.models import User
import re


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15,validators=[validators.validatePhone])
    address = models.CharField(max_length=200,blank=True, null=True, )
    country= models.CharField(max_length=100, blank=True, null=True)
    state= models.CharField(max_length=100, blank=True, null=True)
    city= models.CharField(max_length=100, blank=True, null=True)
    zip_code= models.CharField(max_length=20, blank=True, null=True)
    old_cart = models.TextField(blank=True, null=True)

    
    def __str__(self):
        return f"{self.user.username} Profile"


from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name = re.sub(r"\s+", " ", self.name.lower()).strip()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Categories"
       


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    phone=models.CharField(max_length=15, validators=[validators.validatePhone])

    class Meta:
        verbose_name_plural = "Customers"



    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Product(models.Model):
    name=models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True,default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='category',default=1)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name


class Order(models.Model):
    status_choices = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending',choices=status_choices)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()

    class Meta:
        verbose_name_plural = "Orders"
    
    def __str__(self):
        return f"Order {self.id} - {self.product.name} for {self.customer.first_name}"




