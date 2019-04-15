from django.db import models


# Create your models here.
class Poll(models.Model):
    title = models.CharField(null=False, max_length=255)


class Option(models.Model):
    name = models.CharField(null=False, max_length=255)
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE, null=True, related_name="poll_option")


class Vote(models.Model):
    poll_option = models.ForeignKey('Option', on_delete=models.CASCADE, null=True, related_name="option_vote")
    date_created = models.DateTimeField(auto_now_add=True)
