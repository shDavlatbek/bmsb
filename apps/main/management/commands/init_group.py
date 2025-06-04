from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Create the "Maktab Admin" group if it does not already exist.'

    def handle(self, *args, **options):
        name = "Maktab Admin"
        group, created = Group.objects.get_or_create(name=name)
        if created:
            self.stdout.write(self.style.SUCCESS(f'✔ Created group "{name}".'))
        else:
            self.stdout.write(self.style.WARNING(f'→ Group "{name}" already exists.'))
