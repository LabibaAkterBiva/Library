from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    balance = models.DecimalField(default=500, max_digits=12, decimal_places=2)
    birth_day = models.DateField(null=True, blank=True)
   

    def __str__(self) -> str:
        return self.user.first_name