from django.shortcuts import render
from .models import Product, Supplier
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .forms import ProductForm
from .models import Order
from .forms import OrderForm
from django.contrib import messages

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@user_passes_test(is_admin)
def order_add(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, 'Заказ добавлен.')
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'main/order_form.html', {'form': form, 'title': 'Добавление заказа'})

@user_passes_test(is_admin)
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            messages.success(request, 'Заказ обновлён.')
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'main/order_form.html', {'form': form, 'title': 'Редактирование заказа'})

@user_passes_test(is_admin)
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Заказ удалён.')
        return redirect('order_list')
    return render(request, 'main/order_confirm_delete.html', {'order': order})

def order_list(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'main/order_list.html', {'orders': orders})

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@user_passes_test(is_admin)
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Товар успешно добавлен.')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'main/product_form.html', {'form': form, 'title': 'Добавление товара'})

@user_passes_test(is_admin)
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            if 'image' in request.FILES and product.image:
                product.image.delete(save=False)
            product = form.save()
            messages.success(request, 'Товар успешно обновлён.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'main/product_form.html', {'form': form, 'title': 'Редактирование товара'})

@user_passes_test(is_admin)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.orderitem_set.exists():
        messages.error(request, 'Нельзя удалить товар, который присутствует в заказах.')
        return redirect('product_list')
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Товар удалён.')
        return redirect('product_list')
    return render(request, 'main/product_confirm_delete.html', {'product': product})

def product_list(request):
    products = Product.objects.all()
    
    query = request.GET.get('q', '')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(manufacturer__name__icontains=query) |
            Q(supplier__name__icontains=query)
        )
    
    supplier_id = request.GET.get('supplier', '')
    if supplier_id and supplier_id != 'all':
        products = products.filter(supplier_id=supplier_id)
    
    sort = request.GET.get('sort', '')
    if sort == 'quantity_asc':
        products = products.order_by('quantity_in_stock')
    elif sort == 'quantity_desc':
        products = products.order_by('-quantity_in_stock')
    
    suppliers = Supplier.objects.all()
    
    context = {
        'products': products,
        'suppliers': suppliers,
        'current_query': query,
        'current_supplier': supplier_id,
        'current_sort': sort,
    }
    return render(request, 'main/product_list.html', context)