from django.core.management.base import BaseCommand
from shop.models import Order  # Adjust the import based on your Order model's location

class Command(BaseCommand):
    help = 'Update email addresses for orders that do not have one'

    def handle(self, *args, **kwargs):
        # Filter orders without an email address
        orders_without_email = Order.objects.filter(email='')  # Adjust field name as needed

        for order in orders_without_email:
            # Set a default email; adjust this logic as needed
            default_email = f"order{order.id}@example.com"  # Example placeholder email
            order.email = default_email
            order.save()
            self.stdout.write(self.style.SUCCESS(f'Updated email for order ID {order.id} to {default_email}'))

        self.stdout.write(self.style.SUCCESS('Email update complete!'))
