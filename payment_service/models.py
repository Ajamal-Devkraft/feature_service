from django.db import models

# Create your models here.
class LeadData(models.Model):
    lead_id = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default="Failed")
    source = models.CharField(max_length=255, default="")
