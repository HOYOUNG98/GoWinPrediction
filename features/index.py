import pandas as pd
from scripts.WHR import add_WHR_features
from scripts.against_win_rate import add_against_win_rate_features

from scripts.streak import add_streak_features
from scripts.win_rate import add_win_rate_features

if __name__ == "__main__":

    df = pd.read_csv("../data/processed/data.csv")

    df.sort_values(by=['date'], inplace=True, ignore_index=True)

    df = add_streak_features(df)
    df = add_win_rate_features(df)
    df = add_against_win_rate_features(df)
    df = add_WHR_features(df)

    df.to_csv("../data/processed/engineered.csv", index=False)
