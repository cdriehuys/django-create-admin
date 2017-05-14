from django.core.management import CommandError, call_command
from django.utils.six import StringIO

import pytest

from create_admin.management.commands import createadmin


def test_basic_create(django_user_model):
    """
    The command should be able to create a new admin given a username
    and password.
    """
    out = StringIO()
    call_command('createadmin', username='foo', password='bar', out=out)

    user = django_user_model.objects.get(username='foo')

    assert user.check_password('bar')
    assert user.is_staff
    assert user.is_superuser


def test_get_username_command_flag():
    """
    If only the --username flag is given, that value should be used.
    """
    assert createadmin.Command.get_username(username='foo') == 'foo'


def test_get_username_both(os_env):
    """
    If both the command line flag and environment variables are set, the
    command line flag should take precedence.
    """
    os_env['DJANGO_ADMIN_USERNAME'] = 'bar'

    assert createadmin.Command.get_username(username='foo') == 'foo'


def test_get_username_env(os_env):
    """
    If only the DJANGO_ADMIN_USERNAME environment variable is given,
    that value should be used.
    """
    os_env['DJANGO_ADMIN_USERNAME'] = 'foo'

    assert createadmin.Command.get_username() == 'foo'


def test_no_args():
    """
    If no arguments are given, the script should throw an error giving
    the required arguments.
    """
    out = StringIO()

    with pytest.raises(CommandError) as excinfo:
        call_command('createadmin', out=out)

    assert '--username and --password are required' in str(excinfo.value)


def test_update_password(django_user_model):
    """
    If a user with the given username already exists, their password
    should be updated to the one given.
    """
    user = django_user_model.objects.create_user(
        username='foo',
        password='bar')

    out = StringIO()
    call_command('createadmin', username='foo', password='baz', out=out)

    user.refresh_from_db()
    assert user.check_password('baz')


def test_username_no_password():
    """
    If a username is provided but a password isn't, an error should be
    raised.
    """
    out = StringIO()

    with pytest.raises(CommandError) as excinfo:
        call_command('createadmin', username='foo', out=out)

    expected = '--password is required when a username is given.'

    assert expected in str(excinfo.value)
