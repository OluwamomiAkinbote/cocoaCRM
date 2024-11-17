from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Order, Product, ProductEntry, Category
from shop.forms import ProductEntryForm, ProductForm, CategoryForm
from django.http import JsonResponse
from cities_light.models import Country, Region

@login_required(login_url='/accounts/login/')
def product_entries(request):
    product_id = request.GET.get('product_id')
    
    # Fetch entries related to the selected product owned by the logged-in user
    entries = ProductEntry.objects.filter(product__id=product_id, product__owner=request.user).select_related('product').values(
        'id', 
        'quantity', 
        'selling_price', 
        'product__name'  
    )
    
    # Convert queryset to a list of dictionaries
    entries_list = list(entries)

    # Optionally rename the key for clarity
    for entry in entries_list:
        entry['product_name'] = entry.pop('product__name')

    return JsonResponse(entries_list, safe=False)


@login_required(login_url='/accounts/login/')
def product_list(request):
    products = Product.objects.filter(owner=request.user).prefetch_related('entries')
    categories = Category.objects.filter(owner=request.user)
    
    selected_category_id = request.GET.get('category')
    if selected_category_id:
        products = products.filter(category_id=selected_category_id)
    
    return render(request, 'product/product_list.html', {
        'products': products,
        'categories': categories,
    })


@login_required(login_url='/accounts/login/')
def add_product(request):
    product_form = ProductForm(request.POST or None, request.FILES or None)
    countries = Country.objects.all()
    category_form = CategoryForm()
    categories = Category.objects.filter(owner=request.user)

    if request.method == "POST":
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.owner = request.user  # Ensure product is owned by logged-in user
            product.save()
            messages.success(request, "Product added successfully.")
            return redirect('product_list')

        if 'category_name' in request.POST:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category = category_form.save(commit=False)
                category.owner = request.user  # Ensure category is owned by logged-in user
                category.save()
                messages.success(request, "Category added successfully.")
                return redirect('add_product')

    context = {
        'form': product_form,
        'countries':countries,
        'category_form': category_form,
        'categories': categories
    }
    return render(request, 'product/add_product.html', context)


@login_required(login_url='/accounts/login/')
def add_entry(request):
    if request.method == "POST":
        form = ProductEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            if entry.product.owner == request.user:  # Ensure product belongs to the user
                entry.save()
                messages.success(request, "Product entry added successfully.")
                return redirect('product_list')
            else:
                messages.error(request, "You do not have permission to add entries to this product.")
        else:
            messages.error(request, "Error adding product entry.")
    else:
        form = ProductEntryForm()

    products = Product.objects.filter(owner=request.user)  # Only show products owned by the user
    return render(request, 'product/add_entry.html', {'form': form, 'products': products})


@login_required(login_url='/accounts/login/')
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.owner = request.user  # Ensure category is owned by the logged-in user
            category.save()
            messages.success(request, "Category added successfully.")
            return redirect('add_product')
    return redirect('add_product')


@login_required(login_url='/accounts/login/')
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk, owner=request.user)  # Ensure the category belongs to the user
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect('add_product')
        else:
            messages.error(request, "Error updating category.")
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'product/edit_category.html', {'form': form})


@login_required(login_url='/accounts/login/')
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk, owner=request.user)  # Ensure the category belongs to the user
    category.delete()
    messages.success(request, "Category deleted successfully.")
    return redirect('add_product')


@login_required(login_url='/accounts/login/')
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, owner=request.user)  # Ensure the product belongs to the user
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('product_list')
        else:
            messages.error(request, "Error updating product.")
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'product/edit_product.html', {'form': form, 'product': product})


@login_required(login_url='/accounts/login/')
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, owner=request.user)  # Ensure the product belongs to the user
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('product_list')
    
    return render(request, 'product/delete_product.html', {'product': product})
