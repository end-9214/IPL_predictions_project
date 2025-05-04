import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


def load_data(matches_path, deliveries_path, team_stats_path=None):
    matches = pd.read_csv(matches_path)
    deliveries = pd.read_csv(deliveries_path)
    team_stats = None
    if team_stats_path:
        team_stats = pd.read_csv(team_stats_path)
    return matches, deliveries, team_stats


def determine_home_team(row, team_name):
    if row["city"] in team_name or row["venue"] in team_name:
        return 1
    return 0


def get_venue_win_pct(row, home_pct, away_pct, is_home):
    if is_home == 1:
        return home_pct
    return away_pct


def preprocess_data(matches, deliveries, team_stats=None):
    valid_matches = matches.dropna(subset=["winning_team"]).copy()

    valid_matches.loc[:, "toss_winner_won_match"] = (
        valid_matches["toss_winner"] == valid_matches["winning_team"]
    ).astype(int)

    valid_matches.loc[:, "batting_first_won"] = np.where(
        valid_matches["innings1_score"] > valid_matches["innings2_score"], 1, 0
    )

    team_win_rates = {}
    unique_teams = set(valid_matches["team1"].unique()) | set(
        valid_matches["team2"].unique()
    )
    for team in unique_teams:
        team_matches = valid_matches[
            (valid_matches["team1"] == team) | (valid_matches["team2"] == team)
        ]
        wins = team_matches[team_matches["winning_team"] == team].shape[0]
        team_win_rates[team] = (
            wins / team_matches.shape[0] if team_matches.shape[0] > 0 else 0
        )

    valid_matches.loc[:, "team1_win_rate"] = valid_matches["team1"].map(team_win_rates)
    valid_matches.loc[:, "team2_win_rate"] = valid_matches["team2"].map(team_win_rates)

    if team_stats is not None:
        home_win_pct = dict(zip(team_stats["team"], team_stats["home_win_percentage"]))
        away_win_pct = dict(zip(team_stats["team"], team_stats["away_win_percentage"]))

        team1_is_home = []
        team2_is_home = []

        for _, row in valid_matches.iterrows():
            team1_is_home.append(determine_home_team(row, row["team1"]))
            team2_is_home.append(determine_home_team(row, row["team2"]))

        valid_matches.loc[:, "team1_is_home"] = team1_is_home
        valid_matches.loc[:, "team2_is_home"] = team2_is_home
        valid_matches.loc[:, "team1_home_win_pct"] = valid_matches["team1"].map(
            home_win_pct
        )
        valid_matches.loc[:, "team1_away_win_pct"] = valid_matches["team1"].map(
            away_win_pct
        )
        valid_matches.loc[:, "team2_home_win_pct"] = valid_matches["team2"].map(
            home_win_pct
        )
        valid_matches.loc[:, "team2_away_win_pct"] = valid_matches["team2"].map(
            away_win_pct
        )

        team1_venue_win_pct = []
        team2_venue_win_pct = []

        for _, row in valid_matches.iterrows():
            t1_home_pct = row["team1_home_win_pct"]
            t1_away_pct = row["team1_away_win_pct"]
            t1_is_home = row["team1_is_home"]
            team1_venue_win_pct.append(
                get_venue_win_pct(row, t1_home_pct, t1_away_pct, t1_is_home)
            )

            t2_home_pct = row["team2_home_win_pct"]
            t2_away_pct = row["team2_away_win_pct"]
            t2_is_home = row["team2_is_home"]
            team2_venue_win_pct.append(
                get_venue_win_pct(row, t2_home_pct, t2_away_pct, t2_is_home)
            )

        valid_matches.loc[:, "team1_venue_win_pct"] = team1_venue_win_pct
        valid_matches.loc[:, "team2_venue_win_pct"] = team2_venue_win_pct

    return valid_matches


def prepare_features(matches):
    processed_matches = matches.copy()

    encoders = {}
    cat_cols = ["team1", "team2", "venue", "toss_winner", "toss_decision"]

    for col in cat_cols:
        le = LabelEncoder()
        processed_matches.loc[:, col + "_encoded"] = le.fit_transform(
            processed_matches[col].fillna("Unknown").astype(str)
        )
        encoders[col] = le
    processed_matches.loc[:, "team1_won"] = (
        processed_matches["team1"] == processed_matches["winning_team"]
    ).astype(int)
    features = [
        "team1_encoded",
        "team2_encoded",
        "venue_encoded",
        "toss_winner_encoded",
        "toss_decision_encoded",
        "team1_win_rate",
        "team2_win_rate",
    ]

    if "team1_venue_win_pct" in processed_matches.columns:
        additional_features = [
            "team1_is_home",
            "team2_is_home",
            "team1_venue_win_pct",
            "team2_venue_win_pct",
        ]
        features.extend(additional_features)

    return processed_matches[features], processed_matches["team1_won"], encoders
