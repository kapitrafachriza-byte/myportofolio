from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Membuat grup Editor jika belum ada"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Editor")
        if created:
            self.stdout.write(self.style.SUCCESS('Grup "Editor" berhasil dibuat.'))
        else:
            self.stdout.write('Grup "Editor" sudah ada.')
