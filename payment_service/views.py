from django.shortcuts import render
from rest_framework.views import APIView
from payment_service.models import LeadData
from rest_framework.response import Response
from django.db import transaction
from django.db.models import F
import redis
from django.conf import settings
from contextlib import contextmanager

# r = redis.Redis(host='redis', port=6379, db=0)
# Create your views here.

class ProcessedLeadData(APIView):

    def post(self,request):
        lead_id = request.data.get("lead_id")
        source = request.data.get("source", 'API')
        # with r.lock(f"lead-{lead_id}", timeout=5):
        with transaction.atomic():
            qs = LeadData.objects.select_for_update().filter(lead_id=lead_id)
            last_record = qs.order_by('-id').first()

            if qs:
                LeadData.objects.filter(id=last_record.id).update(
                    status=F('status') + 1,
                    source=source
                )
                last_record.refresh_from_db()
                lead = last_record
            else:
                lead = LeadData.objects.create(
                    lead_id=lead_id,
                    status=1,
                    source=source
                )
        return Response({"lead_id": lead_id,"id":lead.id, "status":last_record.status, "source":last_record.source})


            
