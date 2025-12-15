from django.shortcuts import render
from rest_framework.views import APIView
from payment_service.models import LeadData
from rest_framework.response import Response
from django.db import transaction, IntegrityError
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
            try:
                # 1️⃣ Try to create the record (only ONE thread will succeed)
                lead, created = LeadData.objects.get_or_create(
                    lead_id=lead_id,
                    defaults={
                        "status": 1,
                        "source": source
                    }
                )

                # 2️⃣ If record already exists → increment status safely
                if not created:
                    LeadData.objects.filter(id=lead.id).update(
                        status=F("status") + 1,
                        source=source
                    )
                    lead.refresh_from_db()

            except IntegrityError:
                # 3️⃣ Rare race-condition fallback
                lead = LeadData.objects.select_for_update().get(lead_id=lead_id)
                LeadData.objects.filter(id=lead.id).update(
                    status=F("status") + 1,
                    source=source
                )
                lead.refresh_from_db()

        return Response({"lead_id": lead_id,"id":lead.id, "status":lead.status, "source":lead.source})


            
