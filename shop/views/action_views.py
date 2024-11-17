from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from shop.models import Order
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def cancel_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        order.cancel_order()  # Assuming you have a cancel method defined in your Order model
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@login_required(login_url='/accounts/login/')
def delete_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        order.delete_order()  # This will mark the order as deleted
        
        return JsonResponse({'status': 'success', 'message': 'Order deleted successfully.'})
    return HttpResponseBadRequest('Invalid request method.')

@login_required(login_url='/accounts/login/')
def schedule_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        order.schedule_order()  # Call the method to update the status
        
        return JsonResponse({'status': 'success', 'message': 'Order scheduled successfully.'})
    return HttpResponseBadRequest('Invalid request method.')

@login_required(login_url='/accounts/login/')
def deliver_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        order.deliver_order()  # Call the method to update the status
        
        return JsonResponse({'status': 'success', 'message': 'Order scheduled successfully.'})
    return HttpResponseBadRequest('Invalid request method.')

@login_required(login_url='/accounts/login/')
def restore_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, is_deleted=True)
        order.restore_order()  # This will mark the order as not deleted
        
        return JsonResponse({'status': 'success', 'message': 'Order restored successfully.'})
    return HttpResponseBadRequest('Invalid request method.')
