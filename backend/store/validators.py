from django.core.exceptions import ValidationError
import re

def validatePhone(value):
    if len(value) < 11 or len(value) > 14:
        raise ValidationError(
            ('%(value)s is not a valid phone number'),
            params={'value': value},
        )
    
    pattern=re.compile(r'^(?:\+|0)\d{10,15}$')
    if not pattern.match(value):
        raise ValidationError(
            ('%(value)s is not a valid phone number'),
            params={'value': value},
        )
    
# validatePhone('03451234567')  # Example usage
# validatePhone('+923451234567')  # Example usage
# validatePhone('04A51234567')  # Example usage    
# validatePhone('004923451234567')  # Example usage    