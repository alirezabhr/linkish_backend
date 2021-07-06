from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from .managers import CustomUserManager


class MarketerManager(BaseUserManager):

    def create_marketer(self, username, phone, mail, password=None, **extra_fields):
        marketer = Marketer(username=username, phone=phone, mail=mail, is_active=False, **extra_fields)
        marketer.set_password(password)
        marketer.save()
        return marketer


class InfluencerManager(BaseUserManager):

    def create_influencer(self, username, phone, mail=None, password=None, **extra_fields):
        if mail is None:
            raise TypeError('Users must have an email address.')
        influencer = Influencer(username=username, phone=phone, mail=mail, **extra_fields)
        influencer.set_password(password)
        influencer.save()
        return influencer


# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=11)

    objects = CustomUserManager()  # manager
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return "User: " + self.username

    class Meta:
        verbose_name = "User"


class Marketer(User):
    company_name = models.CharField(max_length=50)
    national_id = models.IntegerField(unique=True)
    company_code = models.IntegerField(unique=True)
    ceo_name = models.CharField(max_length=60)
    telephone = models.CharField(max_length=11)  # e.g:07136234804
    mail = models.EmailField()
    address = models.TextField()

    objects = MarketerManager()

    def __str__(self):
        return "Marketer: " + self.username

    class Meta:
        verbose_name = "Marketer"


class Influencer(User):
    instagram_id = models.CharField(max_length=40, unique=True)
    mail = models.EmailField(blank=True)
    location = models.CharField(max_length=30)  # todo should change it to choice field
    is_general_page = models.BooleanField()
    card_number = models.CharField(max_length=16, null=True)
    account_number = models.CharField(max_length=26, null=True)

    objects = InfluencerManager()
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return "Influencer: " + self.username

    class Meta:
        verbose_name = "Influencer"
