from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator, EmailValidator
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import EmailValidator
from cities_light.models import Country, Region
from djmoney.models.fields import MoneyField

class Category(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category', null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name




class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True)
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    variations = models.CharField(max_length=255, blank=True, null=True)  # Variations such as size, color, etc.

    def __str__(self):
        return self.name


class ProductEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='entries')
    quantity = models.PositiveIntegerField(default=1)
    selling_price = MoneyField(max_digits=14, decimal_places=0, default_currency='USD')  # No decimals

    def __str__(self):
        return f"{self.quantity} of {self.product.name} at {self.selling_price}"

    @property
    def total_amount(self):
        if self.quantity > 0:
            return self.selling_price * self.quantity
        return 0



class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Statuses'

    def __str__(self):
        return self.name


class UserStatusAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='status_actions')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='user_actions')
    action_count = models.IntegerField(default=0)  # Track how many actions the user has performed
    created_at = models.DateTimeField(auto_now_add=True)  # When the action was created

    class Meta:
        pass

    def __str__(self):
        return f"{self.user.username}'s action for {self.status.name}"

    # Increment action count for a user on this status
    def increment_action_count(self):
        self.action_count += 1
        self.save()

    # Decrement action count for a user on this status
    def decrement_action_count(self):
        if self.action_count > 0:
            self.action_count -= 1
            self.save()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_id = models.CharField(max_length=100, unique=True, blank=True, editable=False)
    customer_name = models.CharField(max_length=255, default='')

    # Updated country and state/region fields to use ForeignKey relationships
  
    state_or_region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)

    whatsapp_number = PhoneNumberField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)

    email = models.EmailField(
        max_length=255,
        validators=[EmailValidator(message="Enter a valid email address.")],
        default=''
    )

    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    product_entry = models.ForeignKey('ProductEntry', on_delete=models.CASCADE, related_name='orders', null=True)
    address = models.TextField(default='')
    order_date = models.DateTimeField(auto_now_add=True)

    status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, related_name='orders')

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.customer_name}"



    def save(self, *args, **kwargs):
        """Override save method to generate a unique order ID if not provided."""
        if not self.order_id:
            self.order_id = str(uuid.uuid4()).replace('-', '').upper()[:7]  # Generate a 7-character unique ID
        super(Order, self).save(*args, **kwargs)

    @property
    def total_amount(self):
        """Calculate the total amount for the order."""
        return self.product_entry.total_amount if self.product_entry else 0

    @property
    def total_price(self):
        """Get the total price of the order, can be modified to include discounts in the future."""
        return self.total_amount

    def change_status(self, new_status_name):
        """
        Change the order status, and manage user actions for the current and new status.
        """
        current_status = self.status
        new_status, _ = Status.objects.get_or_create(name=new_status_name)

        # Handle the current user's action for the current status
        if current_status:
            try:
                user_action = UserStatusAction.objects.get(user=self.user, status=current_status)
                user_action.decrement_action_count()  # Decrement the action count for current status
            except UserStatusAction.DoesNotExist:
                pass  # No action exists, so nothing to decrement

        # Update the order status
        self.status = new_status
        self.save()

        # Handle the new user's action for the new status
        user_action, created = UserStatusAction.objects.get_or_create(user=self.user, status=new_status)
        user_action.increment_action_count()  # Increment the action count for new status

    def cancel_order(self):
        """Cancel the order and move it to the 'Cancelled' status."""
        self.change_status('Cancelled')

    def schedule_order(self):
        """Schedule the order and move it to the 'Scheduled' status."""
        self.change_status('Scheduled')

    def deliver_order(self):
        """Schedule the order and move it to the 'Scheduled' status."""
        self.change_status('Delivered')

    def delete_order(self):
        """Soft delete the order by marking it as deleted and moving it to the 'Deleted' status."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.change_status('Deleted')
        self.save()

    def restore_order(self):
        """Restore a deleted order by moving it back to the list of active orders."""
        if self.is_deleted:
            self.is_deleted = False
            self.deleted_at = None
            self.change_status('New')  # Restore to default 'New' status
            self.save()



