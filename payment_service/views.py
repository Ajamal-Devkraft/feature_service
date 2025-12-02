from django.shortcuts import render
from rest_framework.views import APIView
from payment_service.models import LeadData
from rest_framework.response import Response
# Create your views here.

class ProcessedLeadData(APIView):

    def post(self,request):
        lead_id = request.data.get("lead_id")
        if LeadData.objects.filter(lead_id=lead_id).exists():
            lead_data = LeadData.objects.get(lead_id=lead_id)
            status = int(lead_data.status)  + 1
            LeadData.objects.create(lead_id=lead_id, status=status)
        else:
            lead_data = LeadData.objects.create(lead_id=lead_id, status=1)
        return Response({"lead_id": lead_id})


            
