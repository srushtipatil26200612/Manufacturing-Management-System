from django.db import models
from decimal import Decimal

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

class SalesOrder(models.Model):
    order_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )
    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        default='Pending'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.order_number


class Production(models.Model):
    production_number = models.CharField(max_length=20, unique=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    def __str__(self):
        return self.production_number


class QualityCheck(models.Model):
    production = models.ForeignKey(
        Production,
        on_delete=models.CASCADE
    )
    inspection_date = models.DateField(auto_now_add=True)
    inspected_quantity = models.PositiveIntegerField(default=0)
    accepted_quantity = models.PositiveIntegerField(default=0)
    rejected_quantity = models.PositiveIntegerField(default=0)
    result = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Passed', 'Passed'),
            ('Failed', 'Failed'),
        ],
        default='Pending'
    )
    corrective_action = models.TextField(blank=True)

    def __str__(self):
        return f"Quality Check - {self.production.production_number}"


class Dispatch(models.Model):
    sales_order = models.ForeignKey(
        SalesOrder,
        on_delete=models.CASCADE
    )
    dispatch_date = models.DateField()
    transporter = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100, blank=True)
    dispatched_quantity = models.PositiveIntegerField(default=0)
    delivery_status = models.CharField(
        max_length=30,
        choices=[
            ('Pending', 'Pending'),
            ('Dispatched', 'Dispatched'),
            ('In Transit', 'In Transit'),
            ('Delivered', 'Delivered'),
        ],
        default='Pending'
    )

    def __str__(self):
        return f"Dispatch - {self.sales_order.order_number}"



class Invoice(models.Model):
    sales_order = models.ForeignKey(
        SalesOrder,
        on_delete=models.CASCADE
    )
    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    advance_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('Unpaid', 'Unpaid'),
            ('Partially Paid', 'Partially Paid'),
            ('Paid', 'Paid'),
        ],
        default='Unpaid'
    )

    @property
    def outstanding_balance(self):
        total_payments = sum(
            self.payments.values_list('amount', flat=True),
            Decimal('0.00')
        )
        balance = self.total_amount - self.advance_amount - total_payments
        return max(balance, Decimal('0.00'))

    def __str__(self):
        return self.invoice_number

class Payment(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(
        max_length=30,
        choices=[
            ('Cash', 'Cash'),
            ('UPI', 'UPI'),
            ('Bank Transfer', 'Bank Transfer'),
            ('Cheque', 'Cheque'),
        ]
    )
    reference_number = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Payment - {self.invoice.invoice_number}"

class StockTransaction(models.Model):
    raw_material = models.ForeignKey(
        RawMaterial,
        on_delete=models.CASCADE
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=[
            ('IN', 'Stock In'),
            ('OUT', 'Stock Out'),
        ]
    )
    quantity = models.PositiveIntegerField()
    transaction_date = models.DateField(auto_now_add=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.raw_material.name} - {self.transaction_type}"
