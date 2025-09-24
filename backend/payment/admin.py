from django.contrib import admin

# Register your models here.
from .models import ShippingAddress,Order,OrderItem




class OrderInline(admin.StackedInline):
    model = OrderItem
    verbose_name_plural = 'Order Items'
    extra=0

class orderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderInline]




admin.site.register(ShippingAddress)
admin.site.register(Order,orderAdmin)

admin.site.register(OrderItem)