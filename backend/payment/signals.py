from .models import ShippingAddress,Order
from django.db.models.signals import post_save,pre_save

from django.dispatch import receiver

from django.contrib.auth.models import User

import datetime

def create_shipping(sender, instance, created, **kwargs):
	if created:
		user_shipping = ShippingAddress(customer=instance)
		user_shipping.save()

# Automate the profile thing
post_save.connect(create_shipping, sender=User)

#auto add shippin data

def set_shipped_date(sender,instance,**kwargs):
	if instance.pk:
		current_date=datetime.datetime.now()

		obj=sender._default_manager.get(pk=instance.pk)
		if instance.shipped and not obj.shipped:
			instance.date_shipped=current_date




pre_save.connect(set_shipped_date,sender=Order)


