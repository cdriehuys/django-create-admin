from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Command to create/manage admin users.
    """
    help = 'Create an admin user'

    def add_arguments(self, parser):
        """
        Add available options to the parser.
        """
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)

    def handle(*args, **options):
        """
        Create an admin user based on the given options.
        """
        username = options.get('username')
        password = options.get('password')

        user = get_user_model().objects.create_user(
            username=username,
            password=password)

        # Set additional admin flags
        user.is_staff = True
        user.is_superuser = True

        user.save()
