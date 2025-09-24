from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    shipping_full_name=models.CharField(max_length=255)
    shipping_email=models.EmailField(max_length=255,null=True,blank=True)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, blank=True, null=True)
    shipping_city = models.CharField(max_length=100)
    shipping_country = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100,blank=True, null=True)
    shipping_postal_code = models.CharField(max_length=20,blank=True, null=True)

    class Meta:
        verbose_name_plural = "Shipping Addresses"

    def __str__(self):
        return f"{self.shipping_address1}, {self.shipping_city}, {self.shipping_country}"
    




class Order(models.Model):
	# Foreign Key
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	full_name = models.CharField(max_length=250)
	email = models.EmailField(max_length=250)
	shipping_address = models.TextField(max_length=15000)
	amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
	date_ordered = models.DateTimeField(auto_now_add=True,editable=True)	
	stripe_session_id = models.CharField(max_length=255, blank=True, null=True)  # ✅ link to Stripe
	paid=models.BooleanField(default=False)    
	shipped = models.BooleanField(default=False)
	date_shipped = models.DateTimeField(blank=True, null=True)
	
	def __str__(self):
		return f'Order - {str(self.id)}'



class OrderItem(models.Model):
	# Foreign Keys
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

	quantity = models.PositiveBigIntegerField(default=1)
	price = models.DecimalField(max_digits=7, decimal_places=2)


	def __str__(self):
		return f'Order Item - {str(self.id)}'
	
	@property
	def line_total(self):
		return self.quantity * self.price