from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Create Apps"

    def handle(self, *args, **options):
        path = Path("backend", "fixtures", f"all.json")
        args = [
            "dumpdata",
            "recordbin",
            "--natural-primary",
            "--indent=1",
            f"--output={path}",
        ]
        call_command(*args)
