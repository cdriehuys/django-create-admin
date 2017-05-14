from django.core.management import CommandError, call_command
from django.utils.six import StringIO

import pytest


def test_basic_create(django_user_model):
    """
    The command should be able to create a new admin given a username
    and password.
    """
    out = StringIO()
    call_command('create-admin', username='foo', password='bar', out=out)

    user = django_user_model.objects.get(username='foo')

    assert user.check_password('bar')
    assert user.is_staff
    assert user.is_superuser


def test_no_args():
    """
    If no arguments are given, the script should throw an error giving
    the required arguments.
    """
    out = StringIO()

    with pytest.raises(CommandError) as excinfo:
        call_command('create-admin', out=out)

    assert '--username and --password are required' in str(excinfo.value)


def test_username_no_password():
    """
    If a username is provided but a password isn't, an error should be
    raised.
    """
    out = StringIO()

    with pytest.raises(CommandError) as excinfo:
        call_command('create-admin', username='foo', out=out)

    expected = '--password is required when a username is given.'

    assert expected in str(excinfo.value)
