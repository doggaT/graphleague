from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from match.models import Match


@login_required(login_url="login")
def my_stats(request):
    match = Match()

    # riot_api.fetch_summoner_matches_data()
    # riot_api.fetch_match_data()
    return render(request, "my-stats.html")
