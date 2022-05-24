import pandas as pd

if __name__ == "__main__":
    games_df = pd.read_csv("../data/processed/data.csv")

    labeled_df = games_df.drop(['win_name', 'lose_name', 'date'], axis=1)
    labeled_df = labeled_df.rename(columns={
        'win_color': 'player_color', 'lose_color': 'opponent_color', 'win_rank': 'player_rank', 'lose_rank': 'opponent_rank'})
    labeled_df['target'] = 1

    reversed_df = labeled_df.copy(deep=True)
    reversed_df = reversed_df.rename(columns={'player_color': 'opponent_color',
                                              'opponent_color': 'player_color', 'player_rank': 'opponent_rank', 'opponent_rank': 'player_rank'})
    reversed_df['target'] = 0

    processed_df = pd.concat([labeled_df, reversed_df], ignore_index=True)
    processed_df = processed_df[(~processed_df['player_rank'].isin(['Ama.', 'Insei', 'NR'])) & (
        ~processed_df['opponent_rank'].isin(['Ama.', 'Insei', 'NR']))]
    processed_df['player_rank'] = processed_df['player_rank'].apply(
        lambda x: int(x[0]))
    processed_df['opponent_rank'] = processed_df['opponent_rank'].apply(
        lambda x: int(x[0]))
    processed_df['player_color'] = processed_df['player_color'].apply(
        lambda x: 1 if x == 'b' else 0)
    processed_df['opponent_color'] = processed_df['opponent_color'].apply(
        lambda x: 1 if x == 'w' else 0)

    processed_df.to_csv("../data/processed/v1.csv", index=False)
