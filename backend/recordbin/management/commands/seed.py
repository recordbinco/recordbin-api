from django.core.management.base import BaseCommand
from django.core.management import call_command

from pathlib import Path


class Command(BaseCommand):
    help = "Loads all fixtures"

    def handle(self, *args, **options):
        fixture_path = Path("backend", "fixtures", f"all.json")
        args = ["loaddata", fixture_path]
        call_command(*args)
