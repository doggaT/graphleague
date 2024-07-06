from django.shortcuts import render
from overview.models import TierList


def index(request):
    tier_list = TierList()
    tier_list.build_tier_list()
    context = {}
    return render(request, "index.html", context)
