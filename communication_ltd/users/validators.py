import json
import re
from django.core.exceptions import ValidationError

# קריאת קובץ JSON
with open(r'communication_ltd/config.json', 'r') as config_file:
    CONFIG = json.load(config_file)

class CustomPasswordValidator:
    def validate(self, password, user=None):
        policy = CONFIG["password_policy"]
        if len(password) < policy["min_length"]:
            raise ValidationError(f"Password must be at least {policy['min_length']} characters long.")
        if policy["require_uppercase"] and not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if policy["require_lowercase"] and not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if policy["require_number"] and not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one number.")
        if policy["require_special_character"] and not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            raise ValidationError("Password must contain at least one special character.")

    def get_help_text(self):
        return "Your password must follow the configured policy."
