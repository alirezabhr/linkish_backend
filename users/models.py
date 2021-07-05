from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from .managers import MarketerManager


# Create your models here.
class Marketer(AbstractUser):
    mobile_number = models.CharField(max_length=11)
    company_name = models.CharField(max_length=50)
    national_id = models.IntegerField(unique=True)
    company_code = models.IntegerField(unique=True)
    ceo_name = models.CharField(max_length=60)
    telephone = models.CharField(max_length=11)   # 07136234804
    email = models.EmailField()
    is_active = models.BooleanField(default=False)

    objects = MarketerManager()
