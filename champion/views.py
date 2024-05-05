import requests
from django.shortcuts import render
from django.views import View


def champions(request):
    return render(request, "champions.html", {"champions": get_all_champions})


def get_all_champions():
    url = "https://ddragon.leagueoflegends.com/cdn/14.9.1/data/en_US/champion.json"
    response = requests.get(url)
    return response.json()


def champion_details(request, champion):
    url = f"https://ddragon.leagueoflegends.com/cdn/14.9.1/data/en_US/champion/{champion}.json"
    response = requests.get(url)
    return render(request, "champion.html", {"champion": response.json()["data"][f"{champion}"]})
