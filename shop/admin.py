from django.contrib import admin
from .models import Order, Product, Category, Status, ProductEntry, UserStatusAction

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'customer_name', 'email', 'phone_number', 
        'whatsapp_number',  'product_name', 'order_quantity', 
        'total_price', 'order_date', 'state_or_region', 'status', 'is_deleted'
    )
    list_filter = ('order_date', 'state_or_region', 'status', 'is_deleted', )
    search_fields = (
        'customer_name', 'product_entry__product__name', 
        'user__username', 'phone_number', 'whatsapp_number', 
        'email', 'state_or_region'
    )
    ordering = ('-order_date',)
    actions = ['restore_orders']

    def product_name(self, obj):
        """Return the name of the product associated with the order."""
        return obj.product_entry.product.name if obj.product_entry else "No Product"

    def order_quantity(self, obj):
        """Return the quantity of the product in the order."""
        return obj.product_entry.quantity if obj.product_entry else 0

    def get_queryset(self, request):
        """Customize the queryset to exclude soft-deleted orders."""
        queryset = super().get_queryset(request)
        return queryset.filter(is_deleted=False)

    def restore_orders(self, request, queryset):
        """Custom action to restore soft-deleted orders."""
        for order in queryset:
            if order.is_deleted:
                order.restore_order()
                self.message_user(request, f"Order {order.order_id} restored.")
    
    restore_orders.short_description = "Restore selected deleted orders"



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','country', 'category', 'variations')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)

@admin.register(ProductEntry)
class ProductEntryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'selling_price')
    search_fields = ('product__name',)
    list_filter = ('product',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    search_fields = ('name', 'owner__username')

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
@admin.register(UserStatusAction)
class UserStatusActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'action_count', 'created_at')
    search_fields = ('user__username', 'status__name')
    list_filter = ('status',)