from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Order, Product, ProductEntry, Status, UserStatusAction
from django.shortcuts import render, redirect
from shop.forms import OrderForm
from django.http import JsonResponse
from django.db.models import Count,Q
from django.http import JsonResponse
from cities_light.models import Country, Region

from django.db.models import OuterRef, Subquery



@login_required(login_url='/accounts/login/')
def index(request):
    user = request.user
    # Get the selected status from the query parameter (optional filter)
    status_filter = request.GET.get('status', None)

    # Filter orders based on the logged-in user and optionally on status
    orders = Order.objects.filter(user=user)

    if status_filter:
        orders = orders.filter(status__name=status_filter)
    else:
        # By default, exclude orders with certain statuses
        excluded_statuses = ['Cancelled', 'Deleted', 'Scheduled', 'Delivered', 'Restored']
        orders = orders.exclude(status__name__in=excluded_statuses)

    # Retrieve all statuses
    statuses = Status.objects.all()

    # Create a count dictionary for each status showing how many actions have been taken
    status_count = {status.name: 0 for status in statuses}  # Initialize with zero counts

    # Get all action counts for the user from UserStatusAction
    user_actions = UserStatusAction.objects.filter(user=user).values('status__name', 'action_count')

    # Populate the status_count dictionary with actual action counts
    for action in user_actions:
        status_count[action['status__name']] = action['action_count']

    context = {
        'orders': orders.order_by('-order_date'),  # Orders will be sorted by date (most recent first)
        'status_count': status_count,
        'total_orders': orders.count(),  # Now this counts only the active orders
    }
    
    return render(request, 'order/index.html', context)


@login_required(login_url='/accounts/login/')
def add_order(request):
    form = OrderForm()
    countries = Country.objects.all()
    product_entries = []
    selected_product_id = None
    selected_country_id = request.GET.get('country_id')  # Get country_id from request
    selected_country_name = request.GET.get('country_name')  # Get country_name from request
    regions = Region.objects.none()  # Initialize regions

    # Handle product selection for filtering product entries
    if request.method == 'GET':
        selected_product_id = request.GET.get('product_id')
        
        if selected_product_id:
            # Filter ProductEntry based on the selected product and logged-in user
            product_entries = ProductEntry.objects.filter(product_id=selected_product_id, product__owner=request.user)

            # Get the associated country for the selected product
            try:
                selected_product = Product.objects.get(id=selected_product_id)
                selected_country_id = selected_product.country.id  # Get the country ID from the selected product
                
                # Fetch regions using the country ID
                regions = Region.objects.filter(country_id=selected_country_id).values('id', 'name')
            except Product.DoesNotExist:
                selected_product_id = None  # Reset if the product does not exist

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # Set the current user
            
            # Make sure 'product_entry' is passed correctly
            product_entry_id = request.POST.get('product_entry')
            if product_entry_id:
                order.product_entry = get_object_or_404(ProductEntry, id=product_entry_id)
                order.save()
                messages.success(request, "Order placed successfully.")
                return redirect('index')  # Redirect to the order list page after saving
            else:
                messages.error(request, "Please select a product entry.")
        else:
            # Log form errors
            print(form.errors)  # Debug line to see the errors in console
            messages.error(request, "There was an error with your submission. Please correct the errors.")

    # Update the form's product field queryset to show only products owned by the user
    form.fields['product'].queryset = Product.objects.filter(owner=request.user)

    # Render the template with the form, product entries, and regions
    return render(request, 'order/add_order.html', {
        'form': form,
        'countries': countries,
        'product_entries': product_entries,
        'regions': list(regions),  # Pass the filtered regions to the template
        'selected_product_id': selected_product_id,
        'selected_country_id': selected_country_id,  # Pass selected country to the template
        'selected_country_name': selected_country_name  # Pass selected country name to the template
    })




def states(request):
    product_id = request.GET.get('product_id')  # Get product ID from request

    # Initialize an empty queryset for regions
    regions = Region.objects.none()

    if product_id:
        try:
            # Fetch the product by its ID
            product = Product.objects.get(id=product_id)

            # Get the country associated with the product
            country = product.country

            if country:
                # Filter regions based on the exact country name associated with the product
                regions = Region.objects.filter(country__name__iexact=country.name).values('id', 'name')
            else:
                return JsonResponse({"error": "Country not associated with the product"}, status=400)
        
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)

    # Return the filtered regions as a JSON response
    return JsonResponse(list(regions), safe=False)












@login_required(login_url='/accounts/login/')
def edit_order(request, order_id):
    # Change 'owner' to 'user' or the appropriate field that references the user
    order = get_object_or_404(Order, id=order_id, user=request.user)  
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order updated successfully.")
            return redirect('index')
        else:
            messages.error(request, "Error updating Order")
    else:
        form = OrderForm(instance=order)
    
    return render(request, 'order/edit_order.html', {'form': form, 'order': order})













