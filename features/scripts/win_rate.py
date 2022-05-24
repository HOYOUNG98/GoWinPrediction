from tqdm import tqdm


def win_rate(df, player):
    df['result'] = df['win_name'].apply(lambda x: 1 if player == x else 0)

    df.insert(df.shape[1], "num_games", range(1, len(df)+1))
    df['cum_sum'] = df['result'].cumsum()

    df['win_rate'] = df['cum_sum']/df['num_games']
    df['win_rate'] = df['win_rate'].shift()

    df['num_games'] = df['num_games'].shift()

    def assign_win_rate(x, player):
        if player == x['win_name']:
            x['PWR'] = x['win_rate']
            x['PNG'] = x['num_games']
        else:
            x['OWR'] = x['win_rate']
            x['ONG'] = x['num_games']
        return x

    df = df.apply(assign_win_rate, player=player, axis=1)
    return df


def add_win_rate_features(df):
    df['PWR'], df['OWR'], df['PNG'], df['ONG'] = 0, 0, 0, 0

    for player in tqdm(df.win_name.unique()):
        filtered_df = df.loc[(df.win_name == player) |
                             (df.lose_name == player)].copy()

        df.update(win_rate(filtered_df, player))

    return df
