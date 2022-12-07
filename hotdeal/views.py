from django.shortcuts import render
from .models import Deal
from rest_framework import viewsets
from .serializers import DealSerializers

# Create your views here.
def index(requests):
    deals = Deal.objects.all().order_by("-cdate")
    return render(requests, "index.html", {"deals" : deals})

class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializers