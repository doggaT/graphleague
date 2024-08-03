import json
from django.test import TestCase, RequestFactory
from unittest.mock import patch
from champion.models import Champion
from overview.views import summoner_search


class IndexViewTest(TestCase):
    @patch("overview.views.TierList")
    def test_index_view(self, MockTierList):
        champion = Champion().get_all_champions()[0]
        mock_tier_list_instance = MockTierList.return_value
        mock_tier_list_instance.get_rates.return_value = [{
            "champion_id": champion,
            "win_rate": f"{0.5:.2%}",
            "pick_rate": f"{0.31:.2%}",
            "ban_rate": f"{0.68:.2%}"
        }]

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertIn("tier_list", response.context)


class SummonerSearchTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch("overview.views.RiotAPI")
    def test_summoner_search_no_results(self, MockRiotAPI):
        mock_riot_api_instance = MockRiotAPI.return_value
        mock_riot_api_instance.fetch_account_data_by_riot_id.return_value = None

        request = self.factory.get("/summoner_search", {"summonerName": "", "summonerTag": ""})
        response = summoner_search(request)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_response["results"]), 0)
