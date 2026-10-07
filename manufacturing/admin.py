from django.contrib import admin
from .models import Product, Category ,  Supplier ,RawMaterial ,Customer ,Enquiry ,Quotation

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(RawMaterial)
admin.site.register(Customer)
admin.site.register(Enquiry)
admin.site.register(Quotation)