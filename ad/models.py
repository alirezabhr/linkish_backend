from django.db import models

from users.models import Marketer, Influencer, Topic


# Create your models here.
class Ad(models.Model):
    title = models.CharField(max_length=20)
    is_video = models.BooleanField()
    image = models.FileField(blank=False, null=False)
    video = models.FileField(blank=True, null=False)
    base_link = models.CharField(max_length=60)
    clicks = models.IntegerField(default=0)
    marketer = models.ForeignKey(Marketer, on_delete=models.CASCADE)
    max_budget = models.PositiveIntegerField()
    is_general = models.BooleanField()
    topics = models.ManyToManyField(Topic, related_name='Ads')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + ": " + self.title + "-" + self.marketer.company_name


class SuggestAd(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    influencer = models.ForeignKey(Influencer, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)
    report_msg = models.CharField(max_length=30, null=True)
    suggested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['ad', 'influencer']

    def __str__(self):
        return self.ad.title + " --> " + self.influencer.instagram_id


class InfAd(models.Model):
    suggested_ad = models.ForeignKey(SuggestAd, on_delete=models.CASCADE)
    clicks = models.IntegerField(default=0)
    short_link = models.CharField(max_length=7, blank=True)
    approved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + "- instagram: " + self.suggested_ad.influencer.instagram_id
