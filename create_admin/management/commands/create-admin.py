from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """
    Command to create/manage admin users.
    """
    help = 'Create an admin user'

    def add_arguments(self, parser):
        """
        Add available options to the parser.
        """
        parser.add_argument(
            '-u',
            '--username',
            action='store',
            help='The username to create the admin with',
            type=str)
        parser.add_argument(
            '-p',
            '--password',
            action='store',
            help=('The password to give the admin. Only has an effect when '
                  '--username is specified.'),
            type=str)

    def handle(*args, **options):
        """
        Create an admin user based on the given options.
        """
        username = options.get('username')
        password = options.get('password')

        if not username:
            raise CommandError('--username and --password are required.')

        if not password:
            raise CommandError('--password is required when a username is '
                               'given.')

        user = get_user_model().objects.create_user(
            username=username,
            password=password)

        # Set additional admin flags
        user.is_staff = True
        user.is_superuser = True

        user.save()
