import logging
import os
import requests
from dotenv import load_dotenv
from tenacity import retry, wait_fixed, wait_random, retry_if_exception, stop_after_attempt
from api.utils import rate_limit_exceeded, max_retries_exceeded

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
    ACCOUNT_BY_RIOT_ID = "https://{}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{}/{}"

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
        print(response.json())
        return response.json()

    @retry(wait=wait_fixed(60) + wait_random(0, 60), retry=retry_if_exception(rate_limit_exceeded),
           stop=stop_after_attempt(10), reraise=True)
    def fetch_summoner_matches_data(self, region, puuid, match_type=None, queue_id=None, count=20):
        params = {"count": count}

        if queue_id:
            params["queue"] = queue_id

        if match_type:
            params["type"] = match_type

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
           stop=stop_after_attempt(100), reraise=True)
    def fetch_summoner_data(self, platform, summoner_id):
        response = requests.get(self.SUMMONER_URL.format(platform, summoner_id),
                                headers=self.headers())
        response.raise_for_status()
        return response.json()

    @retry(wait=wait_fixed(60) + wait_random(0, 60), retry=retry_if_exception(rate_limit_exceeded),
           stop=stop_after_attempt(10), reraise=True)
    def fetch_account_data_by_riot_id(self, region, game_name, tag_line):
        response = requests.get(self.ACCOUNT_BY_RIOT_ID.format(region, game_name, tag_line),
                                headers=self.headers())
        response.raise_for_status()
        return response.json()

    class Static:
        QUEUES_URL = "https://static.developer.riotgames.com/docs/lol/queues.json"
        SUMMONER_SPELLS_URL = "https://ddragon.leagueoflegends.com/cdn/14.13.1/data/en_US/summoner.json"
        RUNES_URL = "http://ddragon.leagueoflegends.com/cdn/14.13.1/data/en_US/runesReforged.json"

        def fetch_queues(self):
            response = requests.get(self.QUEUES_URL)
            response.raise_for_status()
            return response.json()

        def fetch_summoner_spells(self):
            response = requests.get(self.SUMMONER_SPELLS_URL)
            response.raise_for_status()
            return response.json()

        def fetch_runes(self):
            response = requests.get(self.RUNES_URL)
            response.raise_for_status()
            return response.json()


class Region:
    AMERICAS = ("americas", "Americas")
    ASIA = ("asia", "Asia")
    EUROPE = ("europe", "Europe")
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


class RegionToPlatform:
    AMERICAS = ("AMERICAS", ["br1", "la1", "la2", "na1"])
    ASIA = ("ASIA", ["jp1", "kr", "tw2"])
    EUROPE = ("EUROPE", ["eun1", "euw1", "tr1"])
    SEA = ("SEA", ["oc1", "ph2", "vn2", "sg2", "th2"])

    @classmethod
    def all(cls):
        return [cls.AMERICAS, cls.ASIA, cls.EUROPE, cls.SEA]

    @classmethod
    def get_region(cls, platform):
        for region, platforms in cls.all():
            if platform in platforms:
                return region
        return None


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
