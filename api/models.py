import logging
import os
import requests
from dotenv import load_dotenv
from tenacity import retry, wait_fixed, wait_random, retry_if_exception, stop_after_attempt

from api.utils import rate_limit_exceeded

load_dotenv()
logger = logging.getLogger(__name__)


class RiotAPI:
    RIOT_API_KEY = os.getenv("RIOT_API_KEY")
    GAME_VERSIONS_URL = "https://ddragon.leagueoflegends.com/api/versions.json"
    CHALLENGER_LEAGUES_URL = "https://{}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/{}"
    GRANDMASTER_LEAGUES_URL = "https://{}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/{}"
    MASTER_LEAGUES_URL = "https://{}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/{}"
    LEAGUES_URL = "https://{}.api.riotgames.com/lol/league/v4/entries/{}/{}/{}"
    SUMMONER_URL = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/{}"
    SUMMONER_MATCHES_URL = "https://{}.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids"
    MATCH_URL = "https://{}.api.riotgames.com/lol/match/v5/matches/{}"
    MATCH_TIMELINE_URL = "https://{}.api.riotgames.com/lol/match/v5/matches/{}/timeline"

    def headers(self):
        return {"X-Riot-Token": self.RIOT_API_KEY}

    def get_latest_patch_version(self):
        response = requests.get(self.GAME_VERSIONS_URL)
        latest_version = response.json()[0]
        logger.info(f"Latest game version found: {latest_version}")
        return response.json()[0]

    @retry(wait=wait_fixed(60) + wait_random(0, 60), retry=retry_if_exception(rate_limit_exceeded),
           stop=stop_after_attempt(10), reraise=True)
    def fetch_challenger_league_data(self, platform, queue):
        response = requests.get(self.CHALLENGER_LEAGUES_URL.format(platform, queue),
                                headers=self.headers())
        response.raise_for_status()
        return response.json()

    @retry(wait=wait_fixed(60) + wait_random(0, 60), retry=retry_if_exception(rate_limit_exceeded),
           stop=stop_after_attempt(10), reraise=True)
    def fetch_grandmaster_league_data(self, platform, queue):
        response = requests.get(self.GRANDMASTER_LEAGUES_URL.format(platform, queue),
                                headers=self.headers())
        response.raise_for_status()
        return response.json()

    @retry(wait=wait_fixed(60) + wait_random(0, 60), retry=retry_if_exception(rate_limit_exceeded),
           stop=stop_after_attempt(10), reraise=True)
    def fetch_master_league_data(self, platform, queue):
        response = requests.get(self.MASTER_LEAGUES_URL.format(platform, queue),
                                headers=self.headers())
        response.raise_for_status()
        return response.json()

    @retry(wait=wait_fixed(60) + wait_random(0, 60), retry=retry_if_exception(rate_limit_exceeded),
           stop=stop_after_attempt(10), reraise=True)
    def fetch_league_data(self, platform, queue, tier, division):
        response = requests.get(self.LEAGUES_URL.format(platform, queue, tier, division),
                                headers=self.headers())
        response.raise_for_status()
        return response.json()

    @retry(wait=wait_fixed(60) + wait_random(0, 60), retry=retry_if_exception(rate_limit_exceeded),
           stop=stop_after_attempt(10), reraise=True)
    def fetch_summoner_matches_data(self, region, puuid, queue_id=None, count=100):
        params = {"count": count}

        if queue_id:
            params["queue"] = queue_id

        response = requests.get(self.SUMMONER_MATCHES_URL.format(region, puuid),
                                headers=self.headers(), params=params)
        response.raise_for_status()
        return response.json()

    @retry(wait=wait_fixed(60) + wait_random(0, 60), retry=retry_if_exception(rate_limit_exceeded),
           stop=stop_after_attempt(10), reraise=True)
    def fetch_match_data(self, region, match_id):
        response = requests.get(self.MATCH_URL.format(region, match_id),
                                headers=self.headers())
        response.raise_for_status()
        return response.json()

    @retry(wait=wait_fixed(60) + wait_random(0, 60), retry=retry_if_exception(rate_limit_exceeded),
           stop=stop_after_attempt(10), reraise=True)
    def fetch_match_timeline_data(self, region, match_id):
        response = requests.get(self.MATCH_TIMELINE_URL.format(region, match_id),
                                headers=self.headers())
        response.raise_for_status()
        return response.json()

    @retry(wait=wait_fixed(60) + wait_random(0, 60), retry=retry_if_exception(rate_limit_exceeded),
           stop=stop_after_attempt(10), reraise=True)
    def fetch_summoner_data(self, platform, summoner_id):
        response = requests.get(self.SUMMONER_URL.format(platform, summoner_id),
                                headers=self.headers())
        response.raise_for_status()
        return response.json()


class Region:
    AMERICAS = ("americas", "Americas")
    ASIA = ("asia", "Asia")
    EUROPE = ("europe", "EUROPE")
    SEA = ("sea", "SEA")

    @classmethod
    def get_all_regions_display_names(cls):
        return [value[1] for key, value in cls.__dict__.items() if not key.startswith('_') and isinstance(value, tuple)]

    @classmethod
    def get_all_regions_internal_names(cls):
        return [value[0] for key, value in cls.__dict__.items() if not key.startswith('_') and isinstance(value, tuple)]


class Platform:
    BR1 = ("br1", "BR")
    EUN1 = ("eun1", "EUN")
    EUW1 = ("euw1", "EUW")
    JP1 = ("jp1", "JP")
    KR = ("kr", "KR")
    LA1 = ("la1", "LAN")
    LA2 = ("la2", "LAS")
    NA1 = ("na1", "NA")
    OC1 = ("oc1", "OCE")
    TR1 = ("tr1", "TR")
    PH2 = ("ph2", "PH")
    SG2 = ("sg2", "SG")
    TH2 = ("th2", "TH")
    TW2 = ("tw2", "TW")
    VN2 = ("vn2", "VN")

    @classmethod
    def get_all_platforms_display_names(cls):
        return [value[1] for key, value in cls.__dict__.items() if not key.startswith('_') and isinstance(value, tuple)]

    @classmethod
    def get_all_platforms_internal_names(cls):
        return [value[0] for key, value in cls.__dict__.items() if not key.startswith('_') and isinstance(value, tuple)]


class Ranked:
    SOLO_5x5 = "RANKED_SOLO_5x5"
    FLEX_SR = "RANKED_FLEX_SR"
    FLEX_TT = "RANKED_FLEX_TT"


class Division:
    ONE = "I"
    TWO = "II"
    THREE = "III"
    FOUR = "IV"


class Tier:
    DIAMOND = "DIAMOND"
    EMERALD = "EMERALD"
    PLATINUM = "PLATINUM"
    GOLD = "GOLD"
    SILVER = "SILVER"
    BRONZE = "BRONZE"
    IRON = "IRON"
