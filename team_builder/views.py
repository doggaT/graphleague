from django.shortcuts import render
from team_builder.models import TeamBuilder


def team_builder(request):
    builder = TeamBuilder()
    builder.collect_data()
    builder.apply_kmeans()

    context = {}
    return render(request, "team-builder.html", context)
