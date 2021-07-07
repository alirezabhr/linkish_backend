from django.db import models

from users.models import Marketer, Influencer, Topic


# Create your models here.
class Ad(models.Model):
    title = models.CharField(max_length=20)
    content = models.FileField(blank=False, null=False)
    base_link = models.CharField(max_length=60)
    clicks = models.IntegerField(default=0)
    marketer = models.ForeignKey(Marketer, on_delete=models.CASCADE)
    max_budget = models.PositiveIntegerField()
    topics = models.ManyToManyField(Topic, related_name='Ads')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + ": " + self.title + "-" + self.marketer.company_name


class InfAd(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    influencer = models.ForeignKey(Influencer, on_delete=models.CASCADE)
    clicks = models.IntegerField(default=0)
    short_link = models.CharField(max_length=12)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + ": " + self.influencer.instagram_id
