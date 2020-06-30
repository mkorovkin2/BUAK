from django.db import models
from datetime import datetime

class Filename(models.Model):
    username = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now, blank=True)
    record_count = models.IntegerField(blank=True, null=True)
    class Meta:
        unique_together = ["username", "filename"]
