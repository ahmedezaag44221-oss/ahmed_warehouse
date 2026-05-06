from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product, Transaction
import pandas as pd
import qrcode
import io
import base64

def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()

    # توليد QR Code لكل صنف
    for p in products:
        data = f"الصنف: {p.name} | الكمية: {p.quantity}"
        qr = qrcode.make(data)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        p.qr_code = base64.b64encode(buffer.getvalue()).decode()

    total_items = products.count()
    total_value = sum(p.quantity * p.price for p in products)
    low_stock_count = products.filter(quantity__lt=5).count()
    recent_transactions = Transaction.objects.all().order_by('-date')[:5]

    return render(request, 'stocks/product_list.html', {
        'products': products,
        'total_items': total_items,
        'total_value': total_value,
        'low_stock_count': low_stock_count,
        'recent_transactions': recent_transactions,
    })

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        old_qty = product.quantity
        new_qty = int(request.POST.get('quantity'))
        
        # تسجيل الحركة (صادر أو وارد)
        diff = new_qty - old_qty
        if diff != 0:
            t_type = 'IN' if diff > 0 else 'OUT'
            Transaction.objects.create(product=product, type=t_type, amount=abs(diff))

        product.name = request.POST.get('name')
        product.quantity = new_qty
        product.price = request.POST.get('price')
        product.save()
        return redirect('product_list')
    return render(request, 'stocks/edit_product.html', {'product': product})

def add_product(request):
    if request.method == "POST":
        p = Product.objects.create(
            name=request.POST.get('name'),
            quantity=request.POST.get('quantity'),
            price=request.POST.get('price')
        )
        Transaction.objects.create(product=p, type='IN', amount=p.quantity)
        return redirect('product_list')
    return render(request, 'stocks/add_product.html')

def delete_product(request, product_id):
    get_object_or_404(Product, id=product_id).delete()
    return redirect('product_list')

def export_excel(request):
    products = Product.objects.all().values('name', 'quantity', 'price')
    df = pd.DataFrame(list(products))
    df.columns = ['اسم الصنف', 'الكمية', 'السعر']
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Ahmad_Warehouse.xlsx"'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return response