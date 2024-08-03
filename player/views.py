import time
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from api.models import RiotAPI
from champion.models import Champion
from match.models import Match
from player.utils import get_time_since


@login_required(login_url="login")
def my_stats(request):
    match = Match()
    champions = Champion().get_all_champions()

    response, user_account = match.get_my_matches_by_puuid(request.user.id, queue="ranked")
    queues = RiotAPI().Static().fetch_queues()
    summoner_spells = RiotAPI().Static().fetch_summoner_spells()["data"]
    runes = RiotAPI().Static().fetch_runes()
    parsed_matches = []

    for matches in response:
        m = {}
        for queue in queues:
            if queue["queueId"] == matches["info"]["queueId"]:
                queue_name = " ".join(queue["description"].split(" ")[1::-1])
                m["queue_name"] = queue_name
        game_end = datetime.fromtimestamp(matches["info"]["gameEndTimestamp"] / 1000)
        time_since_end = get_time_since(game_end)
        m["time_since_end"] = time_since_end

        game_duration = time.strftime("%M:%S", time.gmtime(matches["info"]["gameDuration"]))
        m["game_duration"] = game_duration

        match_id = matches["metadata"]["matchId"]
        m["match_id"] = match_id

        participants = matches["info"]["participants"]
        m["participants"] = participants

        for summoner in matches["info"]["participants"]:
            if user_account.puuid == summoner["puuid"]:
                my_info = summoner
                m["my_info"] = my_info

        parsed_matches.append(m)

    context = {
        "matches": parsed_matches,
        "champions": champions,
        "summoner_spells": summoner_spells,
        "runes": runes,
        "user": user_account
    }

    return render(request, "my-stats.html", context)


@login_required(login_url="login")
def my_match_stats(request, match_id):
    riot_api = RiotAPI()
    champions = Champion().get_all_champions()

    queues = RiotAPI().Static().fetch_queues()
    summoner_spells = RiotAPI().Static().fetch_summoner_spells()["data"]
    runes = RiotAPI().Static().fetch_runes()

    context = {
        "champions": champions,
        "summoner_spells": summoner_spells,
        "runes": runes,
    }

    if request.method == "POST":
        region = request.POST.get("region")
        match_id = request.POST.get("match_id")
        puuid = request.POST.get("puuid")

        match = riot_api.fetch_match_data(region, match_id)
        m = {}
        for queue in queues:
            if queue["queueId"] == match["info"]["queueId"]:
                queue_name = " ".join(queue["description"].split(" ")[1::-1])
                m["queue_name"] = queue_name
        game_end = datetime.fromtimestamp(match["info"]["gameEndTimestamp"] / 1000)
        time_since_end = get_time_since(game_end)
        m["time_since_end"] = time_since_end

        game_duration = time.strftime("%M:%S", time.gmtime(match["info"]["gameDuration"]))
        m["game_duration"] = game_duration

        blue_team = {}
        red_team = {}
        blue_total_gold = 0
        red_total_gold = 0
        blue_total_kills = 0
        red_total_kills = 0
        blue_total_assists = 0
        red_total_assists = 0
        blue_total_deaths = 0
        red_total_deaths = 0
        blue_win = False
        red_win = False

        teams = match["info"]["teams"]
        for team in teams:
            if team["teamId"] == 100:
                blue_team["bans"] = team["bans"]
                blue_team["objectives"] = team["objectives"]
            elif team["teamId"] == 200:
                red_team["bans"] = team["bans"]
                red_team["objectives"] = team["objectives"]

        participants = match["info"]["participants"]
        blue_participants = []
        red_participants = []
        for participant in participants:
            if participant["teamId"] == 100:
                blue_participants.append(participant)
                blue_total_gold += participant["goldEarned"]
                blue_total_kills += participant["kills"]
                blue_total_assists += participant["assists"]
                blue_total_deaths += participant["deaths"]
                if participant["win"]:
                    blue_win = True

            elif participant["teamId"] == 200:
                red_participants.append(participant)
                red_total_gold += participant["goldEarned"]
                red_total_kills += participant["kills"]
                red_total_assists += participant["assists"]
                red_total_deaths += participant["deaths"]
                if participant["win"]:
                    red_win = True

        blue_team["total_gold"] = blue_total_gold
        blue_team["total_kills"] = blue_total_kills
        blue_team["total_assists"] = blue_total_assists
        blue_team["total_deaths"] = blue_total_deaths
        blue_team["participants"] = blue_participants
        blue_team["win"] = blue_win

        red_team["total_gold"] = red_total_gold
        red_team["total_kills"] = red_total_kills
        red_team["total_assists"] = red_total_assists
        red_team["total_deaths"] = red_total_deaths
        red_team["participants"] = red_participants
        red_team["win"] = red_win

        m["blue_team"] = blue_team
        m["red_team"] = red_team

        for summoner in match["info"]["participants"]:
            if puuid == summoner["puuid"]:
                my_info = summoner
                m["my_info"] = my_info

        context["match"] = m

    return render(request, "match-details.html", context)
