import joblib
import pandas as pd
import numpy as np


def predict_ipl_match(
    team1, team2, venue, toss_winner, toss_decision, team1_win_rate, team2_win_rate
):
    model = joblib.load("IPL_SCORE_WINNER_PREDICTION_MODEL/saved_models/winner_model.pkl")
    encoders = joblib.load("IPL_SCORE_WINNER_PREDICTION_MODEL/saved_models/encoders.pkl")

    team_stats = pd.read_csv("IPL_SCORE_WINNER_PREDICTION_MODEL/data/teamwise_home_and_away.csv")

    match_data = pd.DataFrame(
        {
            "team1": [team1],
            "team2": [team2],
            "venue": [venue],
            "city": [venue.split(",")[0]],
            "toss_winner": [toss_winner],
            "toss_decision": [toss_decision],
        }
    )

    match_data["team1_win_rate"] = (
        team1_win_rate / 100 if team1_win_rate > 1 else team1_win_rate
    )
    match_data["team2_win_rate"] = (
        team2_win_rate / 100 if team2_win_rate > 1 else team2_win_rate
    )

    home_win_pct = dict(zip(team_stats["team"], team_stats["home_win_percentage"]))
    away_win_pct = dict(zip(team_stats["team"], team_stats["away_win_percentage"]))

    city = match_data.loc[0, "city"]
    venue_name = match_data.loc[0, "venue"]

    match_data["team1_is_home"] = 1 if (city in team1 or venue_name in team1) else 0
    match_data["team2_is_home"] = 1 if (city in team2 or venue_name in team2) else 0

    match_data["team1_home_win_pct"] = home_win_pct.get(team1, 0.5)
    match_data["team1_away_win_pct"] = away_win_pct.get(team1, 0.5)
    match_data["team2_home_win_pct"] = home_win_pct.get(team2, 0.5)
    match_data["team2_away_win_pct"] = away_win_pct.get(team2, 0.5)

    match_data["team1_venue_win_pct"] = (
        match_data["team1_home_win_pct"]
        if match_data["team1_is_home"].iloc[0] == 1
        else match_data["team1_away_win_pct"]
    )
    match_data["team2_venue_win_pct"] = (
        match_data["team2_home_win_pct"]
        if match_data["team2_is_home"].iloc[0] == 1
        else match_data["team2_away_win_pct"]
    )

    for col, encoder in encoders.items():
        match_data[col + "_encoded"] = encoder.transform(match_data[col].astype(str))

    features = [
        "team1_encoded",
        "team2_encoded",
        "venue_encoded",
        "toss_winner_encoded",
        "toss_decision_encoded",
        "team1_win_rate",
        "team2_win_rate",
        "team1_is_home",
        "team2_is_home",
        "team1_venue_win_pct",
        "team2_venue_win_pct",
    ]

    X_pred = match_data[features]
    prediction = model.predict(X_pred)[0]
    win_probability = model.predict_proba(X_pred)[0][1]

    if prediction == 1:
        winning_team = team1
        probability = win_probability
    else:
        winning_team = team2
        probability = 1 - win_probability

    return winning_team, probability
