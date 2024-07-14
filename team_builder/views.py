from django.shortcuts import render
from champion.models import Champion
from team_builder.models import TeamBuilder


def team_builder(request):
    builder = TeamBuilder()
    builder.collect_data()
    builder.apply_kmeans()
    champions = Champion().get_all_champions()

    context = {"champions": champions}
    return render(request, "team-builder.html", context)
