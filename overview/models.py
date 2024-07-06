import logging

from celery.utils.log import get_task_logger
from django.contrib.postgres.fields import ArrayField
from django.db import models, transaction
from api.models import RiotAPI, Platform
from champion.models import Champion
from match.models import Match

platforms = Platform.get_all_platforms_internal_names()
riot_api = RiotAPI()
match = Match()

logger = logging.getLogger(__name__)
celery_logger = get_task_logger(__name__)


class TierList(models.Model):
    objects = models.Manager()

    riot_id = models.OneToOneField(Champion, primary_key=True, on_delete=models.CASCADE)
    games = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    picks = models.PositiveIntegerField(default=0)
    bans = models.PositiveIntegerField(default=0)
    synergy = ArrayField(models.CharField(blank=True), null=True, blank=True)

    @staticmethod
    def save_match_info(champion_id, win=False, pick=False, ban=False):
        with transaction.atomic():
            champion = Champion.objects.get(riot_id=champion_id)
            stats, created = TierList.objects.get_or_create(riot_id=champion)

            stats.games += 1
            if win:
                stats.wins += 1
            if pick:
                stats.picks += 1
            if ban:
                stats.bans += 1
            logger.info(f"Saving stats for champion {champion.riot_id}: win {win}, pick {pick}, ban {ban}")
            stats.save()

    @staticmethod
    def calculate_win_rate(champion_id):
        champion = TierList.objects.get(riot_id=champion_id)
        logger.info(f"Calculating win rate for champion {champion.riot_id}")
        return champion.wins / champion.games if champion.games > 0 else 0

    @staticmethod
    def calculate_ban_rate(champion_id):
        champion = TierList.objects.get(riot_id=champion_id)
        logger.info(f"Calculating ban rate for champion {champion.riot_id}")
        return champion.bans / champion.games if champion.games > 0 else 0

    @staticmethod
    def calculate_pick_rate(champion_id):
        champion = TierList.objects.get(riot_id=champion_id)
        logger.info(f"Calculating pick rate for champion {champion.riot_id}")
        return champion.picks / champion.games if champion.games > 0 else 0

    def build_tier_list(self):
        matches = match.get_matches_by_puuid()
        for m in matches:
            participants = m["info"]["participants"]
            teams = m["info"]["teams"]
            for p in participants:
                champion_id = p["championId"]
                win = p["win"]
                celery_logger.info(f"Attempting to save stats for champion {champion_id}")
                self.save_match_info(champion_id, win=win, pick=True)
            for team in teams:
                for ban in team["bans"]:
                    champion_id = ban["championId"]
                    # if the player did not ban a champion, the champion_id will be -1
                    if champion_id is not -1:
                        celery_logger.info(f"Attempting to save stats for champion {champion_id}")
                        self.save_match_info(champion_id, ban=True)
