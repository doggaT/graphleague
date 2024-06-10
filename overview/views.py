import requests
from django.shortcuts import render
from api.utils import headers


def index(request):
    league = requests.get("https://eun1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5",
                          headers=headers())
    print(league.json())

    response = requests.get(f"https://eun1.api.riotgames.com/lol/summoner/v4/summoners/{league.json()['entries'][0]['summonerId']}",
                            headers=headers())
    print(response.json())

    context = {"all": league.json()}
    return render(request, "index.html", context)
