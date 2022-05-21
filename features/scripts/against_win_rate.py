import pandas as pd
from tqdm import tqdm


def computeAWR(x):
    n = x["num_games"]
    for i in range(0, x["num_games"] + 1):
        if (n - i) - i == x["AS"]:
            return (n - i) / n if x["reverted"] == 1 else i / n


def add_against_win_rate_features(df):

    df['AWR'] = 0

    against_df = df.copy(deep=True)
    against_df["match"] = (
        against_df[["win_name", "lose_name"]].apply(sorted, axis=1).astype(str)
    )

    against_df = against_df.groupby("match")

    for name, group in tqdm(against_df):
        group["tolist"] = [
            str(val) for val in group[["win_name", "lose_name"]].values.tolist()
        ]
        group["reverted"] = group.apply(
            lambda x: 1 if x["tolist"] == name else -1, axis=1)
        group["num_games"] = range(1, len(group) + 1)
        group["AS"] = group["reverted"].rolling(5, min_periods=1).sum()
        group["AWR"] = group.apply(computeAWR, axis=1)

        group = group["AWR"]

        group = group.shift()
        df.update(group)

    return df
