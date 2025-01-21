from django.core.management.base import BaseCommand
from cms.models import User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not User.objects.filter(email='admin@example.com').exists():
            User.objects.create_superuser(username='admin', email='admin@example.com', password='Admin123', role='admin')
            self.stdout.write("Admin user created!")
