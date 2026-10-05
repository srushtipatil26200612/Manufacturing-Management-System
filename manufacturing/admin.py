from django.contrib import admin
from .models import Product, Category ,  Supplier ,RawMaterial

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(RawMaterial)