from django.db import models

# Create your models here.
class LeadData(models.Model):
    lead_id = models.CharField(max_length=255, unique=True)
    status = models.IntegerField(default=1)
    source = models.CharField(max_length=255, default="")
    version = models.IntegerField(default=1)
