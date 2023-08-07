import csv
import os

from django.core.management.base import BaseCommand
from foodgram import settings
from reviews.models import Ingredient


class Command(BaseCommand):
    help = 'Import data from CSV file to Ingredient model'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(
            settings.BASE_DIR, 'data/ingredients.csv')

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                name, measurement_unit = row
                ingredient = Ingredient(
                    name=name, measurement_unit=measurement_unit)
                ingredient.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
