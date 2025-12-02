from django.shortcuts import render
from rest_framework.views import APIView
from payment_service.models import LeadData
from rest_framework.response import Response
from django.db import transaction
# Create your views here.

class ProcessedLeadData(APIView):

    def post(self,request):
        lead_id = request.data.get("lead_id")
        last = LeadData.objects.filter(lead_id=lead_id).order_by('-id').first()
        status = 1 if last is None else last.status + 1
        lead = LeadData.objects.create(lead_id=lead_id, status=status)
        return Response({"lead_id": lead_id})


            
