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
    
class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    contact_number = models.CharField(max_length=10, validators=[length])
    SPECIALTY_CHOICES = [
        ('Cardiology', 'Cardiology'),
        ('Neurology', 'Neurology'),
        ('Orthopedics', 'Orthopedics'),
        ('Oncology', 'Oncology'),
        ('Gynecology', 'Gynecology'),
        ('Nephrology', 'Nephrology'),
        ('Urology', 'Urology'),
        ('Liver Transplant', 'Liver Transplant'),
        ('Gastroenterology', 'Gastroenterology'),
        ('Pulmonology', 'Pulmonology'),
    ]
    specialties = models.CharField(max_length=50, choices=SPECIALTY_CHOICES)

    def __str__(self):
        return self.name