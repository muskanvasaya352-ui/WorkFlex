import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workflex_backend.settings')

# Automatic migration run karne ke liye hook
try:
    from django.core.management import call_command
    import django
    django.setup()
    print("Running automatic migrations on deployment...")
    call_command('migrate', interactive=False)
except Exception as e:
    print(f"Migration auto-run failed or skipped: {e}")

application = get_wsgi_application()