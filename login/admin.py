from django.contrib import admin
from .models import Customer, Product, DrinkBase, DrinkPopping, DrinkFlavour

# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(DrinkBase)
admin.site.register(DrinkPopping)
admin.site.register(DrinkFlavour)
