from django.contrib import admin

from core.models import Product, Order, Sale, User, UserProfile

# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Sale)
admin.site.register(User)
admin.site.register(UserProfile)
