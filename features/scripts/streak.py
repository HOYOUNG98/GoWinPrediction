from tqdm import tqdm


def streak(df, player):
    df['result'] = df['win_name'].apply(lambda x: 1 if player == x else -1)

    grouper = (df['result'] != df['result'].shift()).cumsum()
    df['streak'] = df['result'].groupby(grouper).cumsum().shift()

    def assign_streak(x, player):
        if player == x['win_name']:
            x['PS'] = x['streak']
        else:
            x['OS'] = x['streak']
        return x

    df = df.apply(assign_streak, player=player, axis=1)
    return df


def add_streak_features(df):
    df['PS'], df['OS'], df['streak'] = 0, 0, 0

    for player in tqdm(df.win_name.unique()):
        filtered_df = df.loc[(df.win_name == player) |
                             (df.lose_name == player)].copy()

        df.update(streak(filtered_df, player))

    df.drop(['streak'], axis=1)

    return df
