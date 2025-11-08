import json
import re
from django.core.exceptions import ValidationError

# קריאת קובץ JSON
with open(r'communication_ltd/config.json', 'r') as config_file:
    CONFIG = json.load(config_file)

class CustomPasswordValidator:
    def validate(self, password, user=None):
        string_error = ""
        policy = CONFIG["password_policy"]
        if len(password) < policy["min_length"]:
           string_error +=  f"Password must be at least {policy['min_length']} characters long.\n"
        if policy["require_uppercase"] and not re.search(r'[A-Z]', password):
            string_error += "Password must contain at least one uppercase letter.\n"
        if policy["require_lowercase"] and not re.search(r'[a-z]', password):
            string_error += "Password must contain at least one lowercase letter.\n"
        if policy["require_number"] and not re.search(r'[0-9]', password):
            string_error += "Password must contain at least one number.\n"
        if policy["require_special_character"] and not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            string_error += "Password must contain at least one of: !@#$%^&*(),.?\":{\}|<>.\n"
        if  string_error != "":
            raise ValidationError(string_error)
    def get_help_text(self):
        return "Your password must follow the configured policy."
