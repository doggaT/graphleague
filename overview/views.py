from django.shortcuts import render
from overview.models import TierList


def index(request):
    tier_list = TierList()
    tl = tier_list.get_rates()
    context = {"tier_list": tl}
    return render(request, "index.html", context)
