from django.shortcuts import render
from .models import Deal

# Create your views here.
def index(requests):
    deals = Deal.objects.all().order_by("-cdate")
    return render(requests, "index.html", {"deals" : deals})
