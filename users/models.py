from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from .managers import CustomUserManager


class MarketerManager(BaseUserManager):

    def create_marketer(self, email, password=None, **extra_fields):
        marketer = Marketer(username=email, email=email, **extra_fields)
        marketer.set_password(password)
        marketer.save()
        return marketer


class InfluencerManager(BaseUserManager):

    def create_influencer(self, email, topics=None, password=None, **extra_fields):
        if email is None:
            raise TypeError('Users must have an email address.')
        influencer = Influencer(username=email, email=email, **extra_fields)
        influencer.set_password(password)
        influencer.save()
        if influencer.is_general_page:
            influencer.topics.set([])
        else:
            influencer.topics.set(topics)
        return influencer


# Create your models here.
class Topic(models.Model):
    title = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.title


class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()  # manager
    REQUIRED_FIELDS = []

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
    address = models.TextField()
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = MarketerManager()

    def __str__(self):
        return "Marketer: " + self.username

    class Meta:
        verbose_name = "Marketer"


class Influencer(User):
    instagram_id = models.CharField(max_length=40, unique=True)
    province = models.CharField(max_length=30)
    city = models.CharField(max_length=25)
    is_general_page = models.BooleanField()
    card_number = models.CharField(max_length=16, null=True)
    account_number = models.CharField(max_length=26, null=True)
    topics = models.ManyToManyField(Topic, related_name='Influencer_Topics', blank=True)

    USERNAME_FIELD = 'email'
    objects = InfluencerManager()

    def __str__(self):
        return "Influencer: " + self.username

    class Meta:
        verbose_name = "Influencer"


class OTP(models.Model):
    email = models.EmailField()
    otp_code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Withdraw(models.Model):
    influencer = models.ForeignKey(Influencer, on_delete=models.PROTECT)
    amount = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    request_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.influencer.instagram_id + " -> " + str(self.amount) + "T"
