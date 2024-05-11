from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from champion.models import Champion


class ChampionTestCase(TestCase):
    def test_champion_loader_success(self):
        champions_list = Champion.champion_loader()

        self.assertTrue(champions_list)
        self.assertEqual(champions_list[0]["riot_id"], 266)

    def test_champions_view(self):
        response = self.client.get(reverse("champions"))

        expected_champions = Champion.objects.all().order_by("champion_key")
        actual_champions = response.context["champions"].order_by("champion_key")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "champions.html")
        self.assertQuerySetEqual(actual_champions, expected_champions)

    def test_champion_details_view(self):
        champion_key = "Aatrox"
        response = self.client.get(reverse("champion", kwargs={"champion": champion_key}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "champion.html")

        self.assertEqual(response.context["champion"].champion_key, champion_key)

        self.assertIn("attr_rating_labels", response.context)
        self.assertIn("attr_rating_values", response.context)
