from django.conf import settings


def pytest_configure():
    """
    Configure Django settings as minimally as possible.
    """
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'create_admin',
        ])
