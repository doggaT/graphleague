import json
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from champion.models import Champion
from team_builder.models import TeamBuilder, Draft

logger = logging.getLogger(__name__)


def team_builder(request):
    request.session.pop("draft", None)

    champions = Champion().get_all_champions()
    draft_data = request.session.get("draft", None)

    if draft_data:
        draft = Draft.deserialize(draft_data)
    else:
        draft = Draft()

    blue_banned = draft.get_banned_champions()["blue"]
    red_banned = draft.get_banned_champions()["red"]
    blue_picked = draft.get_picked_champions()["blue"]
    red_picked = draft.get_picked_champions()["red"]
    available_picks = draft.get_available_champions()["available_picks"]
    recommendations = draft.get_recommendations()

    context = {
        "champions": champions,
        "champions_json": json.dumps([{
            "id": champion.riot_id,
            "icon_url": champion.icon_url,
            "champion_name": champion.champion_name
        } for champion in champions]),
        "blue_banned": blue_banned,
        "red_banned": red_banned,
        "blue_picked": blue_picked,
        "red_picked": red_picked,
        "available_picks": available_picks,
        "recommendations": recommendations
    }

    return render(request, "team-builder.html", context)


@csrf_exempt
def champion_select(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            champion_id = data.get("champion_id")
            action = data.get("action")
            team = data.get("team")
            position = "TOP"

            if data.get("position") is not None:
                position = data.get("position").upper()

            draft_data = request.session.get("draft", None)
            if draft_data:
                draft = Draft.deserialize(draft_data)
            else:
                draft = Draft()

            if action == "ban":
                draft.ban_champion(champion_id, team)
            elif action == "pick":
                draft.pick_champion(champion_id, team)
            else:
                return JsonResponse({"success": False, "message": "Invalid action type"})

            blue_banned = draft.get_banned_champions()["blue"]
            red_banned = draft.get_banned_champions()["red"]
            blue_picked = draft.get_picked_champions()["blue"]
            red_picked = draft.get_picked_champions()["red"]
            available_picks = draft.get_available_champions()["available_picks"]

            banned_champions = blue_banned + red_banned

            json_obj = {
                "success": True,
                "blue_banned": blue_banned,
                "red_banned": red_banned,
                "blue_picked": blue_picked,
                "red_picked": red_picked
            }

            if len(banned_champions) == 10:
                builder = TeamBuilder()
                builder.collect_data()
                builder.apply_kmeans()
                recommendations = builder.recommend_champion(available_picks, banned_champions, position)
                draft.save_recommendations(recommendations)
                json_obj["recommendations"] = recommendations

            request.session["draft"] = draft.serialize()

            return JsonResponse(json_obj)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON"})
    return JsonResponse({"success": False, "message": "Invalid request method"})
