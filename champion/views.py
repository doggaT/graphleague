import json
from django.shortcuts import render
from champion.models import Champion


def champions(request):
    all_champions = Champion.objects.all()
    champion_name_query = request.GET.get("champion-name")

    if champion_name_query != "" and champion_name_query is not None:
        all_champions = all_champions.filter(champion_name__icontains=champion_name_query)

    return render(request, "champions.html", {"champions": all_champions})


def champion_details(request, champion):
    champion = Champion.objects.filter(champion_key=champion)[0]
    attr_rating_labels = list(champion.attr_rating.keys())[:-2]
    attr_rating_values = list(champion.attr_rating.values())[:-2]

    return render(request, "champion.html", {
        "champion": champion, "attr_rating_labels": attr_rating_labels, "attr_rating_values": attr_rating_values
    })
