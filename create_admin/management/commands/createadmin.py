import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


# Environment variable names
ENV_PASSWORD = 'DJANGO_ADMIN_PASSWORD'
ENV_USERNAME = 'DJANGO_ADMIN_USERNAME'


class Command(BaseCommand):
    """
    Command to create/manage admin users.
    """
    help = 'Create an admin user'

    @staticmethod
    def get_username(**options):
        """
        Get the admin's username.

        We first check the provided options to see if a username was
        given. If that's not present we fall back to the
        ``DJANGO_ADMIN_USERNAME`` environment variable.

        Args:
            options:
                The options produced from the command's argument parser.

        Returns:
            The admin's username, if it was specifed, and ``None``
            otherwise.
        """
        return options.get('username') or os.environ.get(ENV_USERNAME)

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
        username = Command.get_username(**options)
        password = options.get('password')

        if not username:
            raise CommandError('--username and --password are required.')

        if not password:
            raise CommandError('--password is required when a username is '
                               'given.')

        user, _ = get_user_model().objects.get_or_create(username=username)

        # Set user info
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True

        user.save()
