from django.db import models
from django.core.exceptions import ValidationError

def length(value):
    if len(value) != 10 or not value.isdigit():
        raise ValidationError('Phone number must be exactly 10 digits and numeric.')

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=10, validators=[length])
    
    def __str__(self) -> str:
        return f"name {self.name}"