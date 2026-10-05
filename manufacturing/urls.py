from django.urls import path
from . import views

urlpatterns = [
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
]