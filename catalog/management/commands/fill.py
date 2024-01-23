from django.core.management import BaseCommand

from catalog.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        product_list = [
            {"name": "абобус", "description": "какоето", "images": "", "category": "хлам", "price": 1000, "date_of_creation": "2023-12-18", "date_of_change": "2023-12-18"}
        ]

        product_for_create = []

        for product in product_list:
            product_for_create.append(
                Product(**product))

        Product.objects.all().delete()
        Product.objects.bulk_create(product_for_create)