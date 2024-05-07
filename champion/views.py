import requests
from django.shortcuts import render
from .utils import latest_version


def champions(request):
    return render(request, "champions.html", {"champions": get_all_champions})


def get_all_champions():
    url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version()}/data/en_US/champion.json"
    response = requests.get(url)
    return response.json()


def champion_details(request, champion):
    details_url = f"http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions/{champion}.json"
    details_response = requests.get(details_url)
    details = details_response.json()

    for role in details["roles"]:
        if role.casefold() == "vanguard".casefold() or role.casefold() == "juggernaut".casefold() or \
                role.casefold() == "catcher".casefold() or role.casefold() == "burst".casefold() or \
                role.casefold() == "diver".casefold() or role.casefold() == "battlemage".casefold() or \
                role.casefold() == "artillery".casefold() or role.casefold() == "specialist".casefold() or \
                role.casefold() == "enchanter".casefold() or role.casefold() == "skirmisher".casefold() or \
                role.casefold() == "warden".casefold():
            details["roles"].remove(role)

    attr_rating_labels = [key.capitalize() for key in details["attributeRatings"].keys()][:-2]
    attr_rating_values = [value for value in details["attributeRatings"].values()][:-2]

    return render(request, "champion.html", {
        "champion": details, "attr_rating_labels": attr_rating_labels, "attr_rating_values": attr_rating_values
    })
