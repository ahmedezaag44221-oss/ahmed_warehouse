from django.contrib import admin
from django.urls import path
from stocks.views import product_list, delete_product, add_product, export_excel, edit_product

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product_list, name='product_list'),
    path('delete/<int:product_id>/', delete_product, name='delete_product'),
    path('add/', add_product, name='add_product'),
    path('export/', export_excel, name='export_excel'),
    path('edit/<int:product_id>/', edit_product, name='edit_product'),
]