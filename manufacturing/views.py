from django.shortcuts import render , redirect, get_object_or_404
from decimal import Decimal, InvalidOperation
from django.db import IntegrityError
from django.db import transaction
from django.http import JsonResponse
from .models import Product ,  Category ,Supplier ,RawMaterial ,Customer ,Enquiry ,Quotation ,SalesOrder ,Production ,QualityCheck ,Dispatch ,Invoice,Payment ,StockTransaction
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def product_list(request):
    products = Product.objects.all()

    data = []

    for product in products:
        data.append({
            "id": product.id,
            "name": product.name,
            "product_code": product.product_code,
            "quantity": product.quantity,
            "price": str(product.price),
        })

    return JsonResponse(data, safe=False)

def product_page(request):
    search = request.GET.get('search', '')
    selected_category = request.GET.get('category', '')

    products = Product.objects.all()

    if search:
        products = products.filter(
            name__icontains=search
        ) | products.filter(
            product_code__icontains=search
        )

    if selected_category:
        products = products.filter(category_id=selected_category)

    categories = Category.objects.all()

    return render(request, 'products.html', {
        'products': products,
        'search': search,
        'categories': categories,
        'selected_category': selected_category
    })


def add_product(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        product_code = request.POST.get('product_code')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        category = request.POST.get('category')

        try:
            Product.objects.create(
                name=name,
                product_code=product_code,
                category_id=category,
                quantity=quantity,
                price=price
                
            )

            return redirect('product_page')

        except IntegrityError:
            return render(request, 'add_product.html', {
                'error': 'Product code already exists.',
                'categories': categories
            })

    return render(request, 'add_product.html', {
    'categories': categories
})

def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()

    return redirect('product_page')

def edit_product(request, product_id):
    categories = Category.objects.all()
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.product_code = request.POST.get('product_code')
        product.category_id = request.POST.get('category')
        product.quantity = request.POST.get('quantity')
        product.price = request.POST.get('price')

        try:
            product.save()
            return redirect('product_page')

        except IntegrityError:
            return render(request, 'edit_product.html', {
                'product': product,
                 'categories': categories,
                'error': 'Product code already exists.'
            })

    return render(request, 'edit_product.html', {'product': product , 'categories': categories})


def home(request):
    return render(request, 'home.html')


@login_required
def dashboard(request):
    product_count = Product.objects.count()
    category_count = Category.objects.count()
    supplier_count = Supplier.objects.count()
    raw_material_count = RawMaterial.objects.count()
    customer_count = Customer.objects.count()
    enquiry_count = Enquiry.objects.count()
    quotation_count = Quotation.objects.count()
    sales_order_count = SalesOrder.objects.count()

    production_count = Production.objects.count()
    pending_production_count = Production.objects.filter(
        status='Pending'
    ).count()

    return render(request, 'dashboard.html', {
        'product_count': product_count,
        'category_count': category_count,
        'supplier_count': supplier_count,
        'raw_material_count': raw_material_count,
        'customer_count': customer_count,
        'enquiry_count': enquiry_count,
        'quotation_count': quotation_count,
        'sales_order_count': sales_order_count,
        'production_count': production_count,
        'pending_production_count': pending_production_count,
    })

def dashboard_stats(request):
    return JsonResponse({
        'product_count': Product.objects.count(),
        'category_count': Category.objects.count(),
        'production_count': Production.objects.count(),
        'pending_production_count': Production.objects.filter(
            status='Pending'
        ).count(),
    })


    
def category_page(request):
    categories = Category.objects.all()

    return render(request, 'categories.html', {
        'categories': categories
    })

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        Category.objects.create(name=name)

        return redirect('category_page')

    return render(request, 'add_category.html')

def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()

    return redirect('category_page')

def edit_category(request, category_id):
    category = Category.objects.get(id=category_id)

    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.save()

        return redirect('category_page')

    return render(request, 'edit_category.html', {
        'category': category
    })

def supplier_page(request):
    suppliers = Supplier.objects.all()

    return render(request, 'suppliers.html', {
        'suppliers': suppliers
    })

def add_supplier(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        address = request.POST.get('address')

        Supplier.objects.create(
            name=name,
            contact=contact,
            email=email,
            address=address
        )

        return redirect('supplier_page')

    return render(request, 'add_supplier.html')

def delete_supplier(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    supplier.delete()

    return redirect('supplier_page')

def edit_supplier(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)

    if request.method == 'POST':
        supplier.name = request.POST.get('name')
        supplier.contact = request.POST.get('contact')
        supplier.email = request.POST.get('email')
        supplier.address = request.POST.get('address')

        supplier.save()

        return redirect('supplier_page')

    return render(request, 'edit_supplier.html', {
        'supplier': supplier
    })

def raw_material_page(request):
    raw_materials = RawMaterial.objects.all()

    return render(request, 'raw_materials.html', {
        'raw_materials': raw_materials
    })

def add_raw_material(request):
    suppliers = Supplier.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        material_code = request.POST.get('material_code')
        supplier = request.POST.get('supplier')
        quantity = request.POST.get('quantity')
        unit = request.POST.get('unit')
        price = request.POST.get('price')

        try:
            RawMaterial.objects.create(
                name=name,
                material_code=material_code,
                supplier_id=supplier,
                quantity=quantity,
                unit=unit,
                price=price
            )

            return redirect('raw_material_page')

        except IntegrityError:
            return render(request, 'add_raw_material.html', {
                'error': 'Material code already exists.',
                'suppliers': suppliers
            })

    return render(request, 'add_raw_material.html', {
        'suppliers': suppliers
    })

def edit_raw_material(request, material_id):
    material = RawMaterial.objects.get(id=material_id)
    suppliers = Supplier.objects.all()

    if request.method == 'POST':
        material.name = request.POST.get('name')
        material.material_code = request.POST.get('material_code')
        material.supplier_id = request.POST.get('supplier')
        material.quantity = request.POST.get('quantity')
        material.unit = request.POST.get('unit')
        material.price = request.POST.get('price')

        try:
            material.save()
            return redirect('raw_material_page')

        except IntegrityError:
            return render(request, 'edit_raw_material.html', {
                'material': material,
                'suppliers': suppliers,
                'error': 'Material code already exists.'
            })

    return render(request, 'edit_raw_material.html', {
        'material': material,
        'suppliers': suppliers
    })

def delete_raw_material(request, material_id):
    material = RawMaterial.objects.get(id=material_id)
    material.delete()

    return redirect('raw_material_page')

def customer_page(request):
    customers = Customer.objects.all()

    return render(request, 'customers.html', {
        'customers': customers
    })

def add_customer(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        Customer.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address
        )

        return redirect('customer_page')

    return render(request, 'add_customer.html')

def edit_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)

    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.email = request.POST.get('email')
        customer.phone = request.POST.get('phone')
        customer.address = request.POST.get('address')

        customer.save()

        return redirect('customer_page')

    return render(request, 'edit_customer.html', {
        'customer': customer
    })

def delete_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.delete()

    return redirect('customer_page')

def enquiry_page(request):
    enquiries = Enquiry.objects.all()

    return render(request, 'enquiries.html', {
        'enquiries': enquiries
    })

def add_enquiry(request):
    customers = Customer.objects.all()
    products = Product.objects.all()

    if request.method == 'POST':
        customer = request.POST.get('customer')
        product = request.POST.get('product')
        quantity = request.POST.get('quantity')
        requirements = request.POST.get('requirements')
        status = request.POST.get('status')

        Enquiry.objects.create(
            customer_id=customer,
            product_id=product,
            quantity=quantity,
            requirements=requirements,
            status=status
        )

        return redirect('enquiry_page')

    return render(request, 'add_enquiry.html', {
        'customers': customers,
        'products': products
    })

def edit_enquiry(request, enquiry_id):
    enquiry = Enquiry.objects.get(id=enquiry_id)

    customers = Customer.objects.all()
    products = Product.objects.all()

    if request.method == 'POST':
        enquiry.customer_id = request.POST.get('customer')
        enquiry.product_id = request.POST.get('product')
        enquiry.quantity = request.POST.get('quantity')
        enquiry.requirements = request.POST.get('requirements')
        enquiry.status = request.POST.get('status')

        enquiry.save()

        return redirect('enquiry_page')

    return render(request, 'edit_enquiry.html', {
        'enquiry': enquiry,
        'customers': customers,
        'products': products
    })

def delete_enquiry(request, enquiry_id):
    enquiry = Enquiry.objects.get(id=enquiry_id)
    enquiry.delete()

    return redirect('enquiry_page')

def quotation_page(request):
    quotations = Quotation.objects.all()

    return render(request, 'quotations.html', {
        'quotations': quotations
    })

def add_quotation(request):
    enquiries = Enquiry.objects.all()

    if request.method == 'POST':
        enquiry = request.POST.get('enquiry')
        quotation_number = request.POST.get('quotation_number')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        lead_time = request.POST.get('lead_time')
        version = request.POST.get('version')
        status = request.POST.get('status')

        Quotation.objects.create(
            enquiry_id=enquiry,
            quotation_number=quotation_number,
            quantity=quantity,
            price=price,
            lead_time=lead_time,
            version=version,
            status=status
        )

        return redirect('quotation_page')

    return render(request, 'add_quotation.html', {
        'enquiries': enquiries
    })

def edit_quotation(request, quotation_id):
    quotation = Quotation.objects.get(id=quotation_id)
    enquiries = Enquiry.objects.all()

    if request.method == 'POST':
        quotation.enquiry_id = request.POST.get('enquiry')
        quotation.quotation_number = request.POST.get('quotation_number')
        quotation.quantity = request.POST.get('quantity')
        quotation.price = request.POST.get('price')
        quotation.lead_time = request.POST.get('lead_time')
        quotation.version = request.POST.get('version')
        quotation.status = request.POST.get('status')

        quotation.save()

        return redirect('quotation_page')

    return render(request, 'edit_quotation.html', {
        'quotation': quotation,
        'enquiries': enquiries
    })

def delete_quotation(request, quotation_id):
    quotation = Quotation.objects.get(id=quotation_id)
    quotation.delete()

    return redirect('quotation_page')

@login_required
def sales_order_page(request):
    sales_orders = SalesOrder.objects.all()
    return render(request, 'sales_order_page.html', {
        'sales_orders': sales_orders
    })

@login_required
def add_sales_order(request):
    if request.method == 'POST':
        order_number = request.POST.get('order_number')
        customer_id = request.POST.get('customer')
        quotation_id = request.POST.get('quotation')
        status = request.POST.get('status')
        total_amount = request.POST.get('total_amount')

        if not order_number or not customer_id or not total_amount:
            messages.error(request, 'Please fill all required fields.')
            return redirect('add_sales_order')

        SalesOrder.objects.create(
            order_number=order_number,
            customer_id=customer_id,
            quotation_id=quotation_id or None,
            status=status or 'Pending',
            total_amount=total_amount
        )
        messages.success(request, 'Sales order added successfully!')
        return redirect('sales_order_page')

    customers = Customer.objects.all()
    quotations = Quotation.objects.all()

    return render(request, 'add_sales_order.html', {
        'customers': customers,
        'quotations': quotations
    })

@login_required
def edit_sales_order(request, order_id):
    order = get_object_or_404(SalesOrder, id=order_id)

    if request.method == 'POST':
        order.status = request.POST.get('status')
        order.total_amount = request.POST.get('total_amount')
        order.save()
        messages.success(request, 'Sales order updated successfully!')
        return redirect('sales_order_page')

    return render(request, 'edit_sales_order.html', {
        'order': order
    })


@login_required
def delete_sales_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(SalesOrder, id=order_id)
        order.delete()
        messages.success(request, 'Sales order deleted successfully!')

    return redirect('sales_order_page')


@login_required
def production_page(request):
    productions = Production.objects.all()
    return render(request, 'production_page.html', {
        'productions': productions
    })


@login_required
def add_production(request):
    if request.method == 'POST':
        production_number = request.POST.get('production_number')
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        status = request.POST.get('status')

        Production.objects.create(
            production_number=production_number,
            product_id=product_id,
            quantity=quantity,
            start_date=start_date,
            end_date=end_date or None,
            status=status
        )

        messages.success(request, 'Production added successfully!')
        return redirect('production_page')

    products = Product.objects.all()
    return render(request, 'add_production.html', {
        'products': products
    })


@login_required
def edit_production(request, production_id):
    production = get_object_or_404(Production, id=production_id)

    if request.method == 'POST':
        production.production_number = request.POST.get('production_number')
        production.product_id = request.POST.get('product')
        production.quantity = request.POST.get('quantity')
        production.start_date = request.POST.get('start_date')
        production.end_date = request.POST.get('end_date') or None
        production.status = request.POST.get('status')
        production.save()

        messages.success(request, 'Production updated successfully!')
        return redirect('production_page')

    products = Product.objects.all()
    return render(request, 'edit_production.html', {
        'production': production,
        'products': products
    })


@login_required
def delete_production(request, production_id):
    production = get_object_or_404(Production, id=production_id)

    if request.method == 'POST':
        production.delete()
        messages.success(request, 'Production deleted successfully!')
        return redirect('production_page')

    return redirect('production_page')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def quality_check_page(request):
    quality_checks = QualityCheck.objects.select_related('production').all()

    return render(request, 'quality_checks.html', {
        'quality_checks': quality_checks
    })


@login_required
def add_quality_check(request):
    if request.method == 'POST':
        production_id = request.POST.get('production')
        inspected = int(request.POST.get('inspected_quantity', 0))
        accepted = int(request.POST.get('accepted_quantity', 0))
        rejected = int(request.POST.get('rejected_quantity', 0))
        result = request.POST.get('result')
        corrective_action = request.POST.get('corrective_action', '')

        production = get_object_or_404(Production, id=production_id)

        if inspected <= 0 or accepted < 0 or rejected < 0:
            messages.error(request, 'Please enter valid quantities.')
        elif accepted + rejected != inspected:
            messages.error(
                request,
                'Accepted quantity plus rejected quantity must equal inspected quantity.'
            )
        else:
            QualityCheck.objects.create(
                production=production,
                inspected_quantity=inspected,
                accepted_quantity=accepted,
                rejected_quantity=rejected,
                result=result,
                corrective_action=corrective_action
            )
            messages.success(request, 'Quality check added successfully.')
            return redirect('quality_check_page')

    productions = Production.objects.all()
    return render(request, 'add_quality_check.html', {
        'productions': productions
    })


@login_required
def edit_quality_check(request, quality_check_id):
    quality_check = get_object_or_404(
        QualityCheck,
        id=quality_check_id
    )

    if request.method == 'POST':
        inspected_text = request.POST.get('inspected_quantity', '')
        accepted_text = request.POST.get('accepted_quantity', '')
        rejected_text = request.POST.get('rejected_quantity', '')
        result = request.POST.get('result')
        corrective_action = request.POST.get(
            'corrective_action', ''
        ).strip()

        try:
            inspected = int(inspected_text)
            accepted = int(accepted_text)
            rejected = int(rejected_text)

            if inspected <= 0 or accepted < 0 or rejected < 0:
                messages.error(request, 'Please enter valid quantities.')

            elif accepted + rejected != inspected:
                messages.error(
                    request,
                    'Accepted quantity plus rejected quantity must equal inspected quantity.'
                )

            elif result not in ['Pending', 'Passed', 'Failed']:
                messages.error(request, 'Please select a valid result.')

            else:
                quality_check.inspected_quantity = inspected
                quality_check.accepted_quantity = accepted
                quality_check.rejected_quantity = rejected
                quality_check.result = result
                quality_check.corrective_action = corrective_action
                quality_check.save()

                messages.success(
                    request,
                    'Quality check updated successfully.'
                )
                return redirect('quality_check_page')

        except (ValueError, TypeError):
            messages.error(request, 'Please enter valid quantities.')

    return render(request, 'edit_quality_check.html', {
        'quality_check': quality_check
    })


@login_required
def delete_quality_check(request, quality_check_id):
    if request.method != 'POST':
        return redirect('quality_check_page')

    quality_check = get_object_or_404(
        QualityCheck,
        id=quality_check_id
    )
    quality_check.delete()

    messages.success(
        request,
        'Quality check deleted successfully.'
    )
    return redirect('quality_check_page')



@login_required
def dispatch_page(request):
    dispatches = Dispatch.objects.select_related('sales_order').all()

    return render(request, 'dispatches.html', {
        'dispatches': dispatches
    })

    
@login_required
def add_dispatch(request):
    if request.method == 'POST':
        order_id = request.POST.get('sales_order')
        dispatch_date = request.POST.get('dispatch_date')
        transporter = request.POST.get('transporter', '').strip()
        tracking_number = request.POST.get('tracking_number', '').strip()
        quantity = request.POST.get('dispatched_quantity', 0)
        delivery_status = request.POST.get('delivery_status', 'Pending')

        if not transporter or not dispatch_date:
            messages.error(request, 'Please enter the dispatch date and transporter.')
        else:
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    raise ValueError

                order = get_object_or_404(SalesOrder, id=order_id)

                Dispatch.objects.create(
                    sales_order=order,
                    dispatch_date=dispatch_date,
                    transporter=transporter,
                    tracking_number=tracking_number,
                    dispatched_quantity=quantity,
                    delivery_status=delivery_status
                )
                messages.success(request, 'Dispatch record added successfully.')
                return redirect('dispatch_page')

            except (ValueError, TypeError):
                messages.error(request, 'Please enter a valid dispatched quantity.')

    orders = SalesOrder.objects.all()
    return render(request, 'add_dispatch.html', {
        'orders': orders
    })


@login_required
def edit_dispatch(request, dispatch_id):
    dispatch = get_object_or_404(Dispatch, id=dispatch_id)

    if request.method == 'POST':
        dispatch_date = request.POST.get('dispatch_date', '')
        transporter = request.POST.get('transporter', '').strip()
        tracking_number = request.POST.get('tracking_number', '').strip()
        quantity_text = request.POST.get('dispatched_quantity', '')
        delivery_status = request.POST.get('delivery_status', 'Pending')

        try:
            quantity = int(quantity_text)

            if not dispatch_date or not transporter:
                messages.error(
                    request,
                    'Please enter the dispatch date and transporter.'
                )

            elif quantity <= 0:
                messages.error(
                    request,
                    'Dispatched quantity must be greater than zero.'
                )

            elif delivery_status not in [
                'Pending', 'Dispatched', 'In Transit', 'Delivered'
            ]:
                messages.error(request, 'Please select a valid delivery status.')

            else:
                dispatch.dispatch_date = dispatch_date
                dispatch.transporter = transporter
                dispatch.tracking_number = tracking_number
                dispatch.dispatched_quantity = quantity
                dispatch.delivery_status = delivery_status
                dispatch.save()

                messages.success(
                    request,
                    'Dispatch record updated successfully.'
                )
                return redirect('dispatch_page')

        except (ValueError, TypeError):
            messages.error(
                request,
                'Please enter a valid dispatched quantity.'
            )

    return render(request, 'edit_dispatch.html', {
        'dispatch': dispatch
    })


@login_required
def delete_dispatch(request, dispatch_id):
    if request.method != 'POST':
        return redirect('dispatch_page')

    dispatch = get_object_or_404(Dispatch, id=dispatch_id)
    dispatch.delete()

    messages.success(
        request,
        'Dispatch record deleted successfully.'
    )
    return redirect('dispatch_page')



@login_required
def invoice_page(request):
    invoices = Invoice.objects.select_related('sales_order').all()

    return render(request, 'invoices.html', {
        'invoices': invoices
    })


@login_required
def add_invoice(request):
    if request.method == 'POST':
        order_id = request.POST.get('sales_order')
        invoice_number = request.POST.get('invoice_number', '').strip()
        invoice_date = request.POST.get('invoice_date')
        total_amount = request.POST.get('total_amount', '0')
        advance_amount = request.POST.get('advance_amount', '0')

        try:
            total_amount = Decimal(total_amount)
            advance_amount = Decimal(advance_amount)

            if not invoice_number or not invoice_date:
                messages.error(request, 'Please fill all required fields.')
            elif total_amount <= 0 or advance_amount < 0 or advance_amount > total_amount:
                messages.error(request, 'Please enter valid invoice amounts.')
            else:
                order = get_object_or_404(SalesOrder, id=order_id)

                if advance_amount == total_amount:
                    status = 'Paid'
                elif advance_amount > 0:
                    status = 'Partially Paid'
                else:
                    status = 'Unpaid'

                Invoice.objects.create(
                    sales_order=order,
                    invoice_number=invoice_number,
                    invoice_date=invoice_date,
                    total_amount=total_amount,
                    advance_amount=advance_amount,
                    status=status
                )

                messages.success(request, 'Invoice added successfully.')
                return redirect('invoice_page')

        except (InvalidOperation, ValueError, TypeError):
            messages.error(request, 'Please enter valid invoice details.')

        except IntegrityError:
            messages.error(request, 'This invoice number already exists.')

    orders = SalesOrder.objects.all()
    return render(request, 'add_invoice.html', {'orders': orders})


@login_required
def edit_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    if request.method == 'POST':
        invoice_number = request.POST.get(
            'invoice_number', ''
        ).strip()
        invoice_date = request.POST.get('invoice_date', '')
        total_text = request.POST.get('total_amount', '0')
        advance_text = request.POST.get('advance_amount', '0')
        status = request.POST.get('status', '')

        try:
            total_amount = Decimal(total_text)
            advance_amount = Decimal(advance_text)

            if not invoice_number or not invoice_date:
                messages.error(
                    request, 'Please fill all required fields.'
                )

            elif (
                total_amount <= 0
                or advance_amount < 0
                or advance_amount > total_amount
            ):
                messages.error(
                    request, 'Please enter valid invoice amounts.'
                )

            elif status not in ['Unpaid', 'Partially Paid', 'Paid']:
                messages.error(
                    request, 'Please select a valid invoice status.'
                )

            elif Invoice.objects.filter(
                invoice_number=invoice_number
            ).exclude(id=invoice.id).exists():
                messages.error(
                    request, 'This invoice number already exists.'
                )

            else:
                invoice.invoice_number = invoice_number
                invoice.invoice_date = invoice_date
                invoice.total_amount = total_amount
                invoice.advance_amount = advance_amount
                invoice.status = status
                invoice.save()

                messages.success(
                    request, 'Invoice updated successfully.'
                )
                return redirect('invoice_page')

        except (InvalidOperation, ValueError, TypeError):
            messages.error(
                request, 'Please enter valid invoice details.'
            )

    return render(request, 'edit_invoice.html', {
        'invoice': invoice
    })


@login_required
def delete_invoice(request, invoice_id):
    if request.method != 'POST':
        return redirect('invoice_page')

    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.delete()

    messages.success(
        request,
        'Invoice deleted successfully.'
    )
    return redirect('invoice_page')



@login_required
def payment_page(request):
    payments = Payment.objects.select_related('invoice').all()
    return render(request, 'payments.html', {'payments': payments})

@login_required
def add_payment(request):
    if request.method == 'POST':
        invoice_id = request.POST.get('invoice')
        payment_date = request.POST.get('payment_date')
        amount = request.POST.get('amount', '0')
        payment_method = request.POST.get('payment_method')
        reference_number = request.POST.get('reference_number', '').strip()

        try:
            amount = Decimal(amount)
            invoice = get_object_or_404(Invoice, id=invoice_id)

            if not payment_date:
                messages.error(request, 'Please select payment date.')
            elif amount <= 0:
                messages.error(request, 'Payment amount must be greater than zero.')
            elif amount > invoice.outstanding_balance:
                messages.error(request, 'Payment amount cannot exceed outstanding balance.')
            elif not payment_method:
                messages.error(request, 'Please select a payment method.')
            else:
                Payment.objects.create(
                    invoice=invoice,
                    payment_date=payment_date,
                    amount=amount,
                    payment_method=payment_method,
                    reference_number=reference_number
                )

                total_paid = invoice.advance_amount + sum(
                    invoice.payments.values_list('amount', flat=True)
                )

                if total_paid >= invoice.total_amount:
                    invoice.status = 'Paid'
                elif total_paid > 0:
                    invoice.status = 'Partially Paid'
                else:
                    invoice.status = 'Unpaid'

                invoice.save()
                messages.success(request, 'Payment added successfully.')
                return redirect('payment_page')

        except (InvalidOperation, ValueError, TypeError):
            messages.error(request, 'Please enter valid payment details.')

    invoices = Invoice.objects.all()
    return render(request, 'add_payment.html', {'invoices': invoices})


@login_required
def edit_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    if request.method == 'POST':
        payment_date = request.POST.get('payment_date', '')
        amount_text = request.POST.get('amount', '0')
        payment_method = request.POST.get('payment_method', '')
        reference_number = request.POST.get(
            'reference_number', ''
        ).strip()

        try:
            amount = Decimal(amount_text)
            invoice = payment.invoice

            other_payments = invoice.payments.exclude(
                id=payment.id
            )
            other_paid = sum(
                other_payments.values_list('amount', flat=True),
                Decimal('0.00')
            )

            available_balance = (
                invoice.total_amount
                - invoice.advance_amount
                - other_paid
            )

            if not payment_date:
                messages.error(request, 'Please select payment date.')

            elif amount <= 0:
                messages.error(
                    request, 'Payment amount must be greater than zero.'
                )

            elif amount > available_balance:
                messages.error(
                    request,
                    'Payment amount cannot exceed outstanding balance.'
                )

            elif payment_method not in [
                'Cash', 'UPI', 'Bank Transfer', 'Cheque'
            ]:
                messages.error(
                    request, 'Please select a valid payment method.'
                )

            else:
                payment.payment_date = payment_date
                payment.amount = amount
                payment.payment_method = payment_method
                payment.reference_number = reference_number
                payment.save()

                total_paid = invoice.advance_amount + sum(
                    invoice.payments.values_list('amount', flat=True),
                    Decimal('0.00')
                )

                if total_paid >= invoice.total_amount:
                    invoice.status = 'Paid'
                elif total_paid > 0:
                    invoice.status = 'Partially Paid'
                else:
                    invoice.status = 'Unpaid'

                invoice.save()

                messages.success(
                    request, 'Payment updated successfully.'
                )
                return redirect('payment_page')

        except (InvalidOperation, ValueError, TypeError):
            messages.error(
                request, 'Please enter valid payment details.'
            )

    return render(request, 'edit_payment.html', {
        'payment': payment
    })


@login_required
def delete_payment(request, payment_id):
    if request.method == 'POST':
        payment = get_object_or_404(Payment, id=payment_id)
        invoice = payment.invoice

        payment.delete()

        total_paid = invoice.advance_amount + sum(
            invoice.payments.values_list('amount', flat=True)
        )

        if total_paid >= invoice.total_amount:
            invoice.status = 'Paid'
        elif total_paid > 0:
            invoice.status = 'Partially Paid'
        else:
            invoice.status = 'Unpaid'

        invoice.save()
        messages.success(request, 'Payment deleted successfully.')

    return redirect('payment_page')


@login_required
def reports_page(request):
    context = {
        'total_products': Product.objects.count(),
        'total_customers': Customer.objects.count(),
        'total_orders': SalesOrder.objects.count(),
        'total_production': Production.objects.count(),
        'total_enquiries': Enquiry.objects.count(),
        'total_quotations': Quotation.objects.count(),
        'total_dispatches': Dispatch.objects.count(),
        'total_invoices': Invoice.objects.count(),
        'total_payments': Payment.objects.count(),
        'total_invoice_amount': sum(
            Invoice.objects.values_list('total_amount', flat=True),
            Decimal('0.00')
        ),
        'total_paid_advance': sum(
            Invoice.objects.values_list('advance_amount', flat=True),
            Decimal('0.00')
        ),
    }
    return render(request, 'reports.html', context)


@login_required
def stock_transaction_page(request):
    transactions = StockTransaction.objects.select_related(
        'raw_material'
    ).all().order_by('-transaction_date')

    return render(
        request,
        'stock_transactions.html',
        {'transactions': transactions}
    )


@login_required
def add_stock_transaction(request):
    raw_materials = RawMaterial.objects.all()

    if request.method == 'POST':
        material_id = request.POST.get('raw_material')
        transaction_type = request.POST.get('transaction_type')
        quantity_text = request.POST.get('quantity')
        note = request.POST.get('note', '').strip()

        try:
            quantity = int(quantity_text)
            material = RawMaterial.objects.get(id=material_id)

            if quantity <= 0:
                messages.error(request, 'Quantity must be greater than zero.')

            elif transaction_type not in ['IN', 'OUT']:
                messages.error(request, 'Select a valid transaction type.')

            elif transaction_type == 'OUT' and quantity > material.quantity:
                messages.error(request, 'Insufficient raw material stock.')

            else:
                StockTransaction.objects.create(
                    raw_material=material,
                    transaction_type=transaction_type,
                    quantity=quantity,
                    note=note
                )

                if transaction_type == 'IN':
                    material.quantity += quantity
                else:
                    material.quantity -= quantity

                material.save()
                messages.success(request, 'Stock transaction added successfully.')
                return redirect('stock_transaction_page')

        except (ValueError, TypeError, RawMaterial.DoesNotExist):
            messages.error(request, 'Please enter valid transaction details.')

    return render(
        request,
        'add_stock_transaction.html',
        {'raw_materials': raw_materials}
    )


@login_required
def edit_stock_transaction(request, transaction_id):
    with transaction.atomic():
        stock_transaction = get_object_or_404(
            StockTransaction.objects.select_for_update(),
            id=transaction_id
        )

        raw_materials = RawMaterial.objects.all()

        if request.method == 'POST':
            material_id = request.POST.get('raw_material')
            transaction_type = request.POST.get('transaction_type')
            quantity_text = request.POST.get('quantity')
            note = request.POST.get('note', '').strip()

            try:
                quantity = int(quantity_text)
                material = get_object_or_404(
                    RawMaterial.objects.select_for_update(),
                    id=material_id
                )

                if quantity <= 0:
                    messages.error(
                        request,
                        'Quantity must be greater than zero.'
                    )

                elif transaction_type not in ['IN', 'OUT']:
                    messages.error(
                        request,
                        'Select a valid transaction type.'
                    )

                else:
                    old_material = RawMaterial.objects.select_for_update().get(
                        id=stock_transaction.raw_material_id
                    )

                    # Restore the effect of the old transaction.
                    if stock_transaction.transaction_type == 'IN':
                        old_material.quantity -= stock_transaction.quantity
                    else:
                        old_material.quantity += stock_transaction.quantity

                    # Apply the edited transaction to the selected material.
                    if transaction_type == 'OUT':
                        available = old_material.quantity

                        if material.id != old_material.id:
                            available = material.quantity

                        if quantity > available:
                            messages.error(
                                request,
                                'Insufficient raw material stock.'
                            )
                            return render(
                                request,
                                'edit_stock_transaction.html',
                                {
                                    'stock_transaction': stock_transaction,
                                    'raw_materials': raw_materials
                                }
                            )

                    if material.id == old_material.id:
                        if transaction_type == 'IN':
                            old_material.quantity += quantity
                        else:
                            old_material.quantity -= quantity

                        old_material.save()
                    else:
                        old_material.save()

                        if transaction_type == 'IN':
                            material.quantity += quantity
                        else:
                            material.quantity -= quantity

                        material.save()

                    stock_transaction.raw_material = material
                    stock_transaction.transaction_type = transaction_type
                    stock_transaction.quantity = quantity
                    stock_transaction.note = note
                    stock_transaction.save()

                    messages.success(
                        request,
                        'Stock transaction updated successfully.'
                    )
                    return redirect('stock_transaction_page')

            except (ValueError, TypeError):
                messages.error(
                    request,
                    'Please enter valid transaction details.'
                )

    return render(
        request,
        'edit_stock_transaction.html',
        {
            'stock_transaction': stock_transaction,
            'raw_materials': raw_materials
        }
    )

@login_required
def delete_stock_transaction(request, transaction_id):
    if request.method != 'POST':
        return redirect('stock_transaction_page')

    with transaction.atomic():
        stock_transaction = get_object_or_404(
            StockTransaction.objects.select_for_update(),
            id=transaction_id
        )

        material = get_object_or_404(
            RawMaterial.objects.select_for_update(),
            id=stock_transaction.raw_material_id
        )

        # Reverse the effect of the original transaction.
        if stock_transaction.transaction_type == 'IN':
            material.quantity -= stock_transaction.quantity
        else:
            material.quantity += stock_transaction.quantity

        if material.quantity < 0:
            messages.error(
                request,
                'Cannot delete this transaction because stock would become negative.'
            )
            return redirect('stock_transaction_page')

        material.save()
        stock_transaction.delete()

    messages.success(
        request,
        'Stock transaction deleted successfully.'
    )
    return redirect('stock_transaction_page')


