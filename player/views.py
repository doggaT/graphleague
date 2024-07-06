import time
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from api.models import RiotAPI
from match.models import Match
from player.utils import get_time_since


@login_required(login_url="login")
def my_stats(request):
    match = Match()

    response, user_account = match.get_my_matches_by_puuid(request.user.id, queue="ranked")
    queues = RiotAPI().Static().fetch_queues()
    parsed_matches = []

    for matches in response:
        for queue in queues:
            if queue["queueId"] == matches["info"]["queueId"]:
                queue_name = " ".join(queue["description"].split(" ")[1::-1])
                parsed_matches.append(queue_name)

        game_end = datetime.fromtimestamp(matches["info"]["gameEndTimestamp"] / 1000)
        time_since_end = get_time_since(game_end)
        parsed_matches.append(time_since_end)

        game_duration = time.strftime("%M:%S", time.gmtime(matches["info"]["gameDuration"]))
        parsed_matches.append(game_duration)

        participants = matches["info"]["participants"]
        parsed_matches.append(participants)

        for summoner in matches["info"]["participants"]:
            if user_account.puuid == summoner["puuid"]:
                my_info = summoner
                parsed_matches.append(my_info)

    context = {"matches": parsed_matches}
    return render(request, "my-stats.html", context)
