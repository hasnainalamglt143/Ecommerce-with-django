from django.contrib import admin
from . import models
from django.contrib.auth.models import User
from store.models import Profile, Category, Customer, Product, Order

# Register your models here.
# Change admin site titles
admin.site.site_header = "Ecommerce Center Admin"          # Top-left header
admin.site.site_title = "commerce Center Admin Admin Portal"    # Browser tab title
admin.site.index_title = "Welcome to commerce Center Dashboard"  

class ProfileInline(admin.StackedInline):
    model = Profile
    verbose_name_plural = 'Profile'

class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [ProfileInline]


# unregister old model
admin.site.unregister(User)

#register new User model with Profile inline
admin.site.register(User, UserAdmin)
admin.site.register(Profile)  # Register your models here.

admin.site.register(models.Category)  # Register your models here.
admin.site.register(models.Customer)  # Register your models here.
admin.site.register(models.Product)  # Register your models here.
admin.site.register(models.Order)  # Register your models here.