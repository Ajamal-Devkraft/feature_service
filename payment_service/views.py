from django.shortcuts import render
from rest_framework.views import APIView
from payment_service.models import LeadData
from rest_framework.response import Response
# Create your views here.

class ProcessedLeadData(APIView):

    def post(self,request):
        lead_id = request.data.get("lead_id")
        status = request.data.get("status")
        if LeadData.objects.filter(lead_id=lead_id).exists():
            lead_data = LeadData.objects.get(lead_id=lead_id)
            lead_data.status = status
            lead_data.save()
        else:
            lead_data = LeadData.objects.create(lead_id=lead_id, status=status)
        return Response({"lead_id": lead_id, "status": status})


            
