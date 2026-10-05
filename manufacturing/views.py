from django.shortcuts import render , redirect
from django.db import IntegrityError
from django.http import JsonResponse
from .models import Product ,  Category ,Supplier


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
    product_count = Product.objects.count()
    category_count = Category.objects.count()

    return render(request, 'home.html', {
        'product_count': product_count,
        'category_count': category_count
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