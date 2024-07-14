import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from django.db.models import F
from overview.models import TierList


class TeamBuilder:
    def __init__(self):
        self.df = None
        self.kmeans = None
        self.scaler = StandardScaler()

    def ban_phase(self):
        pass

    def pick_phase(self):
        pass

    def collect_data(self):
        champions = TierList.objects.annotate(champion_id=F("riot_id_id")).all()
        data = []
        for champion in champions:
            data.append({
                "champion_id": champion.champion_id,
                "win_rate": champion.wins / champion.games if champion.games > 0 else 0,
                "pick_rate": champion.picks / champion.games if champion.games > 0 else 0,
                "ban_rate": champion.bans / champion.games if champion.games > 0 else 0,
            })
        self.df = pd.DataFrame(data)

    def preprocess_data(self):
        features = ["win_rate", "pick_rate", "ban_rate"]
        X = self.df[features]
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled

    def apply_kmeans(self, n_clusters=5):
        X_scaled = self.preprocess_data()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.df['cluster'] = self.kmeans.fit_predict(X_scaled)

    def recommend_champion(self, available_champions, banned_champions):
        available_df = self.df[self.df["champion_id"].isin(available_champions)]
        available_df = available_df[~available_df["champion_id"].isin(banned_champions)]

        if available_df.empty:
            return None

        best_cluster = available_df.loc[available_df["win_rate"].idxmax()]["cluster"]

        recommendation = \
            available_df[available_df["cluster"] == best_cluster].sort_values(by="win_rate", ascending=False).iloc[0]

        return recommendation["champion_id"]
