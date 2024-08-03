import time
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from api.models import RiotAPI, Platform, RegionToPlatform
from champion.models import Champion
from match.models import Match
from overview.models import TierList
from player.utils import get_time_since


def index(request):
    tier_list = TierList()
    tl = tier_list.get_rates()
    context = {"tier_list": tl}
    return render(request, "index.html", context)


def summoner_search(request):
    riot_api = RiotAPI()
    static_api = RiotAPI.Static()
    platforms = Platform().get_all_platforms()
    regions = RegionToPlatform()

    name = request.GET.get("summonerName")
    tag = request.GET.get("summonerTag", "")

    results = []
    summoner_level = 0
    unique_ids = set()
    if name and tag:
        for platform in platforms:
            region = regions.get_region(platform[0])
            result = riot_api.fetch_account_data_by_riot_id(region, game_name=name, tag_line=tag)
            if result is not None:
                summoner_details = riot_api.fetch_summoner_data_by_puuid(platform[0], result["puuid"])
                if summoner_details is not None and summoner_details["summonerLevel"] > summoner_level:
                    summoner_level = summoner_details["summonerLevel"]
                    info = {
                        "puuid": result["puuid"],
                        "game_name": result["gameName"],
                        "tag_line": result["tagLine"],
                        "summoner_level": summoner_details["summonerLevel"],
                        "platform": platform[1],
                        "region": region,
                        "profile_icon_url": static_api.fetch_profile_icon_url(riot_api.get_latest_patch_version(),
                                                                              summoner_details["profileIconId"])
                    }
                    results.clear()
                    results.append(info)
    elif name and not tag:
        for platform in platforms:
            region = regions.get_region(platform[0])
            result = riot_api.fetch_account_data_by_riot_id(region, game_name=name, tag_line=platform[1])
            if result is not None:
                if result["puuid"] not in unique_ids:
                    unique_ids.add(result["puuid"])
                    summoner_details = riot_api.fetch_summoner_data_by_puuid(platform[0], result["puuid"])
                    info = {
                        "puuid": result["puuid"],
                        "game_name": result["gameName"],
                        "tag_line": result["tagLine"],
                        "summoner_level": summoner_details["summonerLevel"],
                        "platform": platform[1],
                        "region": region,
                        "profile_icon_url": static_api.fetch_profile_icon_url(riot_api.get_latest_patch_version(),
                                                                              summoner_details["profileIconId"])
                    }
                    results.append(info)

    return JsonResponse({"results": results})


def summoner_info(request, puuid):

    if request.method == "POST":
        region = request.POST.get("region")
        match = Match()
        champions = Champion().get_all_champions()

        response = match.get_summoner_matches(region, puuid, queue="ranked")
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
                if puuid == summoner["puuid"]:
                    my_info = summoner
                    m["my_info"] = my_info

            parsed_matches.append(m)

        context = {
            "matches": parsed_matches,
            "champions": champions,
            "summoner_spells": summoner_spells,
            "runes": runes,
            "region": region
        }

        return render(request, "summoner-details.html", context)


def summoner_match(request, match_id, puuid):
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
