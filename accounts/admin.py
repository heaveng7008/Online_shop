from django.contrib import admin
from .models import Customer,Product,Order,Category,Brand

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Brand)
