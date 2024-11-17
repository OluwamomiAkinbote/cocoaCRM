import uuid
from django.core.management.base import BaseCommand
from shop.models import Order

class Command(BaseCommand):
    help = 'Update order IDs for orders that have default order_id values'

    def handle(self, *args, **kwargs):
        orders = Order.objects.filter(order_id='not provided')
        for order in orders:
            order.order_id = str(uuid.uuid4()).replace('-', '').upper()[:7]
            order.save()
            self.stdout.write(self.style.SUCCESS(f'Updated order_id for Order {order.id}'))
