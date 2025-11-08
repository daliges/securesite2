from django.apps import AppConfig
from django.db.utils import OperationalError
from django.core.management import call_command

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        try:
            from users.models import User  # Import model inside function to avoid circular import issues
            if User.objects.exists():  # Check if the table exists
                User.objects.update(is_blocked=False, action_count=0)
        except OperationalError:
            print("Database is not ready, skipping user updates.")
        except Exception as e:
            print(f"Unexpected error in ready(): {e}")
