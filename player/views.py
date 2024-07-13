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

    context = {"matches": parsed_matches, "champions": champions, "summoner_spells": summoner_spells, "runes": runes}
    return render(request, "my-stats.html", context)
