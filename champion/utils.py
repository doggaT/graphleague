import requests


def latest_version():
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    response = requests.get(url)
    return response.json()[0]
