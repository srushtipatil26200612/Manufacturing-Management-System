from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name 

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class RawMaterial(models.Model):
    name = models.CharField(max_length=100)
    material_code = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

        
class Product(models.Model):
    name = models.CharField(max_length=100)
    product_code = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(
    Category,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Enquiry(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)
    requirements = models.TextField(blank=True)
    status = models.CharField(max_length=50, default='New')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.product.name}"

class Quotation(models.Model):
    enquiry = models.ForeignKey(
        Enquiry,
        on_delete=models.CASCADE
    )
    quotation_number = models.CharField(
        max_length=50,
        unique=True
    )
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    lead_time = models.CharField(max_length=100)
    version = models.IntegerField(default=1)
    status = models.CharField(
        max_length=50,
        default='Draft'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.quotation_number