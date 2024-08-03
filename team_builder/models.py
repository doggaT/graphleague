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
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


class TeamBuilder:
    def __init__(self, user_matches, user_account):
        self.df = None
        self.kmeans = None
        self.user_matches = user_matches
        self.user_account = user_account
        self.scaler = StandardScaler()

    def collect_user_match_data(self):
        parsed_matches = []

        if len(self.user_matches) > 0:
            for matches in self.user_matches:
                m = {}
                for summoner in matches["info"]["participants"]:
                    if self.user_account.puuid == summoner["puuid"]:
                        m["champion_id"] = summoner["championId"]
                        m["win"] = summoner["win"]
                        m["kda"] = summoner["challenges"]["kda"]
                        m["position"] = summoner["challenges"]["individualPosition"]
                        m["team_damage_percentage"] = summoner["challenges"]["teamDamagePercentage"]

                parsed_matches.append(m)

        return parsed_matches

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

        user_data = self.collect_user_match_data()
        data = []
        for champion in champions:
            d = {
                "champion_id": champion.champion_id,
                "win_rate": champion.wins / champion.games if champion.games > 0 else 0,
                "pick_rate": champion.picks / champion.games if champion.games > 0 else 0,
                "ban_rate": champion.bans / champion.games if champion.games > 0 else 0,
                "play_rate_top": champion.play_rate_top,
                "play_rate_jungle": champion.play_rate_jungle,
                "play_rate_middle": champion.play_rate_middle,
                "play_rate_bottom": champion.play_rate_bottom,
                "play_rate_utility": champion.play_rate_utility,
            }
            if len(self.user_matches) > 0:
                for match in user_data:
                    if d["champion_id"] == match["champion_id"]:
                        if match["win"]:
                            d["win_rate"] = 1
                        d["kda"] = match["kda"]
                        d["team_damage_percentage"] = match["team_damage_percentage"]
                        d[f"play_rate_{match['position'].lower()}"] = 1
                        d["user_match_weight"] = 1

            data.append(d)
        self.df = pd.DataFrame(data)

    def preprocess_data(self):
        features = [
            "win_rate", "pick_rate", "play_rate_top", "play_rate_jungle", "play_rate_middle", "play_rate_bottom",
            "play_rate_utility"
        ]

        if len(self.user_matches) > 0:
            features.extend(["kda", "team_damage_percentage", "user_match_weight"])

        X = self.df[features]
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled

    def silhouette_analysis(self, max_clusters=10):
        X_scaled = self.preprocess_data()
        silhouette_scores = []

        for n_clusters in range(2, max_clusters + 1):
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(X_scaled)
            silhouette_avg = silhouette_score(X_scaled, cluster_labels)
            silhouette_scores.append((n_clusters, silhouette_avg))

        plt.figure(figsize=(10, 6))
        plt.plot([score[0] for score in silhouette_scores], [score[1] for score in silhouette_scores], marker='o')
        plt.title("Silhouette Analysis")
        plt.xlabel("Number of clusters")
        plt.ylabel("Silhouette score")
        plt.show()

        best_n_clusters = max(silhouette_scores, key=lambda x: x[1])[0]
        print(f"Optimal number of clusters: {best_n_clusters}")

        return best_n_clusters

    def apply_kmeans(self, n_clusters=6):
        X_scaled = self.preprocess_data()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.df["cluster"] = self.kmeans.fit_predict(X_scaled)

    def recommend_champion(self, available_champions, banned_champions, recommend_position, num_clusters=6):
        position_map = {
            "TOP": "play_rate_top",
            "JUNGLE": "play_rate_jungle",
            "MIDDLE": "play_rate_middle",
            "BOTTOM": "play_rate_bottom",
            "SUPPORT": "play_rate_utility"
        }

        available_df = self.df[self.df["champion_id"].isin(available_champions)]
        available_df = available_df[~available_df["champion_id"].isin(banned_champions)]

        if available_df.empty:
            return None

        position_column = position_map[recommend_position]
        available_df = available_df[available_df[position_column] > 0]

        if available_df.empty:
            return None

        if len(self.user_matches) > 0:
            available_df["priority_score"] = available_df["win_rate"] * 0.8 + available_df["kda"] * 0.1 + available_df[
                "team_damage_percentage"] * 0.1
        else:
            available_df["priority_score"] = available_df["win_rate"]

        win_rate_clusters = available_df.groupby("cluster")["priority_score"].mean().sort_values(ascending=False)
        top_clusters = win_rate_clusters.head(num_clusters).index

        recommendations = available_df[available_df["cluster"].isin(top_clusters)].sort_values(by="priority_score",
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
        self.user_account = None
        self.user_matches = []

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

    def save_user_info(self, user_matches, user_account):
        self.user_matches = user_matches
        self.user_account = user_account

    def get_banned_champions(self):
        return {"blue": self.blue_bans, "red": self.red_bans}

    def get_picked_champions(self):
        return {"blue": self.blue_picks, "red": self.red_picks}

    def get_available_champions(self):
        return {"available_picks": self.available_picks}

    def get_recommendations(self):
        return {"recommendations": self.recommendations}

    def get_user_matches(self):
        return {"user_matches": self.user_matches}

    def get_user_account(self):
        return {"user_account": self.user_account}

    def serialize(self):
        return {
            "blue_bans": self.blue_bans,
            "red_bans": self.red_bans,
            "blue_picks": self.blue_picks,
            "red_picks": self.red_picks,
            "available_picks": self.available_picks,
            "recommendations": self.recommendations,
            "user_matches": self.user_matches,
            "user_account": self.user_account
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
        draft.user_matches = data.get("user_matches", [])
        draft.user_account = data.get("user_account", None)
        return draft
