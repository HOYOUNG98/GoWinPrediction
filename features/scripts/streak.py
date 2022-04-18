import pandas as pd
from tqdm import tqdm


def streak(df):
    df['result'] = df['win_name'].apply(lambda x: 1 if player == x else -1)

    grouper = (df['result'] != df['result'].shift()).cumsum()
    df['streak'] = df['result'].groupby(grouper).cumsum().shift()

    df = df.apply(assign_streak, player=player, axis=1)
    return df


def assign_streak(x, player):
    if player == x['win_name']:
        x['PS'] = x['streak']
    else:
        x['OS'] = x['streak']
    return x


if __name__ == "__main__":

    games_df = pd.read_csv("../../data/processed/data.csv")

    games_df.sort_values(by=['date'], inplace=True, ignore_index=True)
    games_df['PS'], games_df['OS'] = 0, 0
    games_df['streak'] = 0

    for player in tqdm(games_df.win_name.unique()):
        filtered_df = games_df.loc[
            (games_df.win_name == player) | (games_df.lose_name == player)
        ].copy()

        df = streak(filtered_df)
        games_df.update(df)

    games_df.drop(['streak'], axis=1)

    games_df.to_csv("../../data/processed/v2.csv", index=False)
