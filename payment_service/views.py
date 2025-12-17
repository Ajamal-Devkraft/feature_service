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
        version = request.data.get("version")
        # with r.lock(f"lead-{lead_id}", timeout=5):
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT pg_advisory_xact_lock(%s)",
                    [int(lead_id)]
                )

            last_record = (
                LeadData.objects
                .select_for_update()
                .filter(lead_id=lead_id)
                .order_by('-id')
                .first()
            )
            if last_record:
                updated = LeadData.objects.filter(id=last_record.id, version=version).update(
                    status=F("status") + 1,
                    version=F("version") + 1,
                    source=source
                )
                if updated == 0:
                    return Response(
                        {"error": "State changed, please refresh and retry"},
                        status=409
                    )
            else:
                lead = LeadData.objects.create(
                    lead_id=lead_id,
                    status=1,
                    source=source,
                    version=version
                )
        return Response({"lead_id": lead_id})
    
    def get(self,request):
        lead_id = request.query_params.get("lead_id")
        lead = LeadData.objects.filter(lead_id=lead_id).last()
        if lead:
            return Response({"lead_id": lead.lead_id, "status": lead.status, "source": lead.source, "version": lead.version})
        else:
            return Response({"error": "Lead not found", "version": 1})


            
