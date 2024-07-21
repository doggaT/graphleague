import logging
import pandas as pd
from django.db.models import FloatField
from django.db.models.functions import Cast
from django.db.models.fields.json import KeyTextTransform
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from django.db.models import F
from champion.models import Champion
from overview.models import TierList

logger = logging.getLogger(__name__)


class TeamBuilder:
    def __init__(self):
        self.df = None
        self.kmeans = None
        self.scaler = StandardScaler()

    def collect_data(self):
        champions = TierList.objects.annotate(
            champion_id=F("riot_id__riot_id"),
            play_rate_top=Cast(KeyTextTransform("playRate",
                                                KeyTextTransform("TOP", "riot_id__overall_play_rates")),
                               FloatField()),
            play_rate_jungle=Cast(KeyTextTransform("playRate",
                                                   KeyTextTransform("JUNGLE", "riot_id__overall_play_rates")),
                                  FloatField()),
            play_rate_middle=Cast(KeyTextTransform("playRate",
                                                   KeyTextTransform("MIDDLE", "riot_id__overall_play_rates")),
                                  FloatField()),
            play_rate_bottom=Cast(KeyTextTransform("playRate",
                                                   KeyTextTransform("BOTTOM", "riot_id__overall_play_rates")),
                                  FloatField()),
            play_rate_utility=Cast(KeyTextTransform("playRate",
                                                    KeyTextTransform("UTILITY", "riot_id__overall_play_rates")),
                                   FloatField())
        ).all()

        data = []
        for champion in champions:
            data.append({
                "champion_id": champion.champion_id,
                "win_rate": champion.wins / champion.games if champion.games > 0 else 0,
                "pick_rate": champion.picks / champion.games if champion.games > 0 else 0,
                "ban_rate": champion.bans / champion.games if champion.games > 0 else 0,
                "play_rate_top": champion.play_rate_top,
                "play_rate_jungle": champion.play_rate_jungle,
                "play_rate_middle": champion.play_rate_middle,
                "play_rate_bottom": champion.play_rate_bottom,
                "play_rate_utility": champion.play_rate_utility,
            })
        self.df = pd.DataFrame(data)

    def preprocess_data(self):
        features = [
            "win_rate", "pick_rate", "play_rate_top", "play_rate_jungle", "play_rate_middle", "play_rate_bottom",
            "play_rate_utility"
        ]
        X = self.df[features]
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled

    def apply_kmeans(self, n_clusters=5):
        X_scaled = self.preprocess_data()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.df["cluster"] = self.kmeans.fit_predict(X_scaled)

    def recommend_champion(self, available_champions, banned_champions, recommend_position):
        position_map = {
            "TOP": "play_rate_top",
            "JUNGLE": "play_rate_jungle",
            "MIDDLE": "play_rate_middle",
            "BOTTOM": "play_rate_bottom",
            "SUPPORT": "play_rate_utility"
        }

        print(recommend_position)

        available_df = self.df[self.df["champion_id"].isin(available_champions)]
        available_df = available_df[~available_df["champion_id"].isin(banned_champions)]

        if available_df.empty:
            return None

        position_column = position_map[recommend_position]
        available_df = available_df[available_df[position_column] > 0]

        if available_df.empty:
            return None

        best_cluster = available_df.loc[available_df["win_rate"].idxmax()]["cluster"]

        recommendations = available_df[available_df["cluster"] == best_cluster].sort_values(by="win_rate",
                                                                                            ascending=False).head(5)

        return recommendations["champion_id"].tolist()


class Draft:
    def __init__(self):
        champions = Champion().get_all_champions()
        self.blue_bans = []
        self.red_bans = []
        self.blue_picks = []
        self.red_picks = []
        self.recommendations = []
        self.available_picks = [champion.riot_id for champion in champions]

    def ban_champion(self, champion_id, team):
        if team == "blue":
            self.blue_bans.append(champion_id)
        elif team == "red":
            self.red_bans.append(champion_id)
        else:
            logger.error(f"Invalid parameters {champion_id} or {team}")
            return

        self.make_champion_unavailable(champion_id)

    def pick_champion(self, champion_id, team):
        if team == "blue":
            self.blue_picks.append(champion_id)
        elif team == "red":
            self.red_picks.append(champion_id)
        else:
            logger.error(f"Invalid parameters {champion_id} or {team}")
            return

        self.make_champion_unavailable(champion_id)

    def make_champion_unavailable(self, champion_id):
        self.available_picks.remove(int(champion_id))

    def save_recommendations(self, recommendations):
        self.recommendations.clear()
        self.recommendations.extend(recommendations)

    def get_banned_champions(self):
        return {"blue": self.blue_bans, "red": self.red_bans}

    def get_picked_champions(self):
        return {"blue": self.blue_picks, "red": self.red_picks}

    def get_available_champions(self):
        return {"available_picks": self.available_picks}

    def get_recommendations(self):
        return {"recommendations": self.recommendations}

    def serialize(self):
        return {
            "blue_bans": self.blue_bans,
            "red_bans": self.red_bans,
            "blue_picks": self.blue_picks,
            "red_picks": self.red_picks,
            "available_picks": self.available_picks,
            "recommendations": self.recommendations
        }

    @classmethod
    def deserialize(cls, data):
        draft = cls()
        draft.blue_bans = data.get("blue_bans", [])
        draft.red_bans = data.get("red_bans", [])
        draft.blue_picks = data.get("blue_picks", [])
        draft.red_picks = data.get("red_picks", [])
        draft.available_picks = data.get("available_picks", [])
        draft.recommendations = data.get("recommendations", [])
        return draft
