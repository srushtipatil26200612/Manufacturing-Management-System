from django.urls import path
from . import views

urlpatterns = [
    path(
    'dashboard-stats/',
    views.dashboard_stats,
    name='dashboard_stats'
),
     path('products/', views.product_list, name='product_list'),
     path('products-page/', views.product_page, name='product_page'),
     path('add-product/', views.add_product, name='add_product'),
     path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
     path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
     path('categories/', views.category_page, name='category_page'),
     path('add-category/', views.add_category, name='add_category'),
     path(
    'delete-category/<int:category_id>/',
    views.delete_category,
    name='delete_category'
),
path(
    'edit-category/<int:category_id>/',
    views.edit_category,
    name='edit_category'
),
path('suppliers/', views.supplier_page, name='supplier_page'),
path('add-supplier/', views.add_supplier, name='add_supplier'),
path('delete-supplier/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),
path('edit-supplier/<int:supplier_id>/', views.edit_supplier, name='edit_supplier'),
path('raw-materials/', views.raw_material_page, name='raw_material_page'),
path('add-raw-material/', views.add_raw_material, name='add_raw_material'),
path('edit-raw-material/<int:material_id>/', views.edit_raw_material, name='edit_raw_material'),
path('delete-raw-material/<int:material_id>/', views.delete_raw_material, name='delete_raw_material'),
path('customers/', views.customer_page, name='customer_page'),
path('add-customer/', views.add_customer, name='add_customer'),
path('edit-customer/<int:customer_id>/', views.edit_customer, name='edit_customer'),
path('delete-customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),
path('enquiries/', views.enquiry_page, name='enquiry_page'),
path('add-enquiry/', views.add_enquiry, name='add_enquiry'),
path(
    'edit-enquiry/<int:enquiry_id>/',
    views.edit_enquiry,
    name='edit_enquiry'
),
path(
    'delete-enquiry/<int:enquiry_id>/',
    views.delete_enquiry,
    name='delete_enquiry'
),
path('quotations/', views.quotation_page, name='quotation_page'),
path('add-quotation/', views.add_quotation, name='add_quotation'),
path(
    'edit-quotation/<int:quotation_id>/',
    views.edit_quotation,
    name='edit_quotation'
),
path(
    'delete-quotation/<int:quotation_id>/',
    views.delete_quotation,
    name='delete_quotation'
),
path('sales-orders/', views.sales_order_page, name='sales_order_page'),
path('sales-orders/add/', views.add_sales_order, name='add_sales_order'),
path('sales-orders/edit/<int:order_id>/', views.edit_sales_order, name='edit_sales_order'),
path('sales-orders/delete/<int:order_id>/', views.delete_sales_order, name='delete_sales_order'),
path('production/', views.production_page, name='production_page'),

path('add-production/', views.add_production, name='add_production'),
path('edit-production/<int:production_id>/', views.edit_production, name='edit_production'),
path('delete-production/<int:production_id>/', views.delete_production, name='delete_production'),
path('register/', views.register_view, name='register'),
path('quality-checks/', views.quality_check_page, name='quality_check_page'),

path('add-quality-check/', views.add_quality_check, name='add_quality_check'),

path(
    'quality-checks/<int:quality_check_id>/edit/',
    views.edit_quality_check,
    name='edit_quality_check'
),

path(
    'quality-checks/<int:quality_check_id>/delete/',
    views.delete_quality_check,
    name='delete_quality_check'
),


path('dispatches/', views.dispatch_page, name='dispatch_page'),
path('add-dispatch/', views.add_dispatch, name='add_dispatch'),

path(
    'dispatches/<int:dispatch_id>/edit/',
    views.edit_dispatch,
    name='edit_dispatch'
),

path(
    'dispatches/<int:dispatch_id>/delete/',
    views.delete_dispatch,
    name='delete_dispatch'
),


path('invoices/', views.invoice_page, name='invoice_page'),
path('add-invoice/', views.add_invoice, name='add_invoice'),

path(
    'invoices/<int:invoice_id>/edit/',
    views.edit_invoice,
    name='edit_invoice'
),

path(
    'invoices/<int:invoice_id>/delete/',
    views.delete_invoice,
    name='delete_invoice'
),


path('payments/', views.payment_page, name='payment_page'),
path('add-payment/', views.add_payment, name='add_payment'),

path(
    'payments/<int:payment_id>/edit/',
    views.edit_payment,
    name='edit_payment'
),

path(
    'payments/<int:payment_id>/delete/',
    views.delete_payment,
    name='delete_payment'
),


path('reports/', views.reports_page, name='reports_page'),
path(
    'stock-transactions/',
    views.stock_transaction_page,
    name='stock_transaction_page'
),
path(
    'add-stock-transaction/',
    views.add_stock_transaction,
    name='add_stock_transaction'
),

path(
    'stock-transactions/<int:transaction_id>/edit/',
    views.edit_stock_transaction,
    name='edit_stock_transaction'
),
path(
    'stock-transactions/<int:transaction_id>/delete/',
    views.delete_stock_transaction,
    name='delete_stock_transaction'
),

]