import pandas as pd
from tqdm import tqdm


def win_rate(df, player):
    df['result'] = df['win_name'].apply(lambda x: 1 if player == x else 0)

    df.insert(df.shape[1], "num_games", range(1, len(df)+1))
    df['cum_sum'] = df['result'].cumsum()

    df['win_rate'] = df['cum_sum']/df['num_games']
    df['win_rate'] = df['win_rate'].shift()

    df = df.apply(assign_win_rate, player=player, axis=1)
    return df


def assign_win_rate(x, player):
    if player == x['win_name']:
        x['PWR'] = x['win_rate']
    else:
        x['OWR'] = x['win_rate']
    return x


if __name__ == "__main__":
    games_df = pd.read_csv("../../data/processed/v2.csv")

    games_df.sort_values(by=['date'], inplace=True, ignore_index=True)

    games_df['PWR'], games_df['OWR'] = 0, 0

    for player in tqdm(games_df.win_name.unique()):
        filtered_df = games_df.loc[
            (games_df.win_name == player) | (games_df.lose_name == player)
        ].copy()

        df = win_rate(filtered_df, player)
        games_df.update(df)

    games_df.to_csv("../../data/processed/v2.csv", index=False)
