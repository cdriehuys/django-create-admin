from django.core.management import call_command
from django.utils.six import StringIO


def test_basic_create(django_user_model):
    """
    The command should be able to create a new admin given a username
    and password.
    """
    out = StringIO()
    call_command('create-admin', 'foo', 'bar', out=out)

    user = django_user_model.objects.get(username='foo')

    assert user.check_password('bar')
    assert user.is_staff
    assert user.is_superuser
