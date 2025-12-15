from django.shortcuts import render
from rest_framework.views import APIView
from payment_service.models import LeadData
from rest_framework.response import Response
from django.db import transaction, connection
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
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT pg_advisory_xact_lock(%s)",
                    [int(lead_id)]
                )

            last_record = (
                LeadData.objects
                .filter(lead_id=lead_id)
                .order_by('-id')
                .first()
            )

            if last_record:
                LeadData.objects.filter(id=last_record.id).update(
                    status=F("status") + 1,
                    source=F("source") + "," + source
                )
                last_record.refresh_from_db()
                lead = last_record
            else:
                lead = LeadData.objects.create(
                    lead_id=lead_id,
                    status=1,
                    source=source
                )
        return Response({"lead_id": lead_id,"id":lead.id, "status":lead.status, "source":lead.source})


            
