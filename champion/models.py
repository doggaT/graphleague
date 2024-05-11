import requests
import logging
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.db import connection


class Champion(models.Model):
    objects = models.Manager()

    riot_id = models.IntegerField(primary_key=True)
    champion_key = models.CharField(null=False)
    champion_name = models.CharField(null=False)
    champion_title = models.CharField(null=False)
    splash_url = models.CharField(null=False)
    icon_url = models.CharField(null=False)
    resource = models.CharField(null=False)
    attack_type = models.CharField(null=False)
    adaptive_type = models.CharField(null=False)
    stats = models.JSONField(null=False)
    positions = ArrayField(models.CharField(null=False))
    roles = ArrayField(models.CharField(null=False))
    role_class = ArrayField(models.CharField(null=False))
    attr_rating = models.JSONField(null=False)
    abilities = models.JSONField(null=False)
    lore = models.CharField(null=False)
    faction = models.CharField(null=False)
    overall_play_rates = models.JSONField(null=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=False)

    @staticmethod
    def champion_loader():
        logger = logging.getLogger(__name__)
        champions = "http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions.json"
        champion_rates = "http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/championrates.json"
        champions_list = []

        try:
            logger.info(f"Loading data from '{champions}' and '{champion_rates}'.")

            champions_response = requests.get(champions)
            champion_rates_response = requests.get(champion_rates)

            champions_data = champions_response.json()
            champion_rates_data = champion_rates_response.json()

            for key, champions_item in champions_data.items():
                role_classes = ["vanguard", "catcher", "diver", "artillery", "enchanter", "warden", "juggernaut",
                                "burst", "battlemage", "specialist", "skirmisher"]
                role_class = []
                champion_rates = champion_rates_data["data"][str(champions_item.get("id"))]

                roles = champions_item["roles"]
                for role in roles:
                    if role.casefold() in role_classes:
                        role_class.append(role)
                        roles.remove(role)

                champion_object = {
                    "riot_id": champions_item.get("id"),
                    "champion_key": champions_item.get("key"),
                    "champion_name": champions_item.get("name"),
                    "champion_title": champions_item.get("title"),
                    "splash_url": f"https://ddragon.leagueoflegends.com/cdn/img/champion/loading/"
                                  f"{champions_item.get('key')}_0.jpg",
                    "icon_url": champions_item.get("icon"),
                    "resource": champions_item.get("resource"),
                    "attack_type": champions_item.get("attackType"),
                    "adaptive_type": champions_item.get("adaptiveType"),
                    "stats": champions_item.get("stats"),
                    "positions": champions_item.get("positions"),
                    "roles": roles,
                    "role_class": role_class,
                    "abilities": champions_item.get("abilities"),
                    "lore": champions_item.get("lore"),
                    "faction": champions_item.get("faction"),
                    "attr_rating": champions_item.get("attributeRatings"),
                    "overall_play_rates": champion_rates
                }

                champions_list.append(champion_object)

        except Exception as e:
            logger.error(f"Failed to read data from {champions} and {champion_rates}: {e}")

        return champions_list
