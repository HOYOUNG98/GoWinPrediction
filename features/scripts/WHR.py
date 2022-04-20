import pandas as pd
from whr import whole_history_rating
from tqdm import tqdm
import datetime


def convergeWHR(df):
    whr = whole_history_rating.Base({'w2': 14, 'uncased': True})
    start_date = datetime.datetime(1941, 5, 18)
    for idx, row in tqdm(df.iterrows()):
        date = datetime.datetime.strptime(row['date'], '%Y-%m-%d')
        delta = date - start_date
        if row['win_color'] == 'b':
            whr.create_game(row['win_name'],
                            row['lose_name'], 'B', delta.days, 0)
        else:
            whr.create_game(row['lose_name'],
                            row['win_name'], 'W', delta.days, 0)

    whr.auto_iterate()
    return whr


if __name__ == "__main__":
    games_df = pd.read_csv("../../data/processed/v2.csv")

    games_df.sort_values(by=['date'], inplace=True, ignore_index=True)

    whr = convergeWHR(games_df)

    games_df['WWHR'], games_df['WWHR-Error'], games_df['LWHR'], games_df['LWHR-Error'] = 0, 0, 0, 0
    for player in tqdm(games_df.win_name.unique()):
        winner_df = games_df.loc[games_df.win_name == player].copy()

        loser_df = games_df.loc[games_df.lose_name == player].copy()

        rating_map, uncertainty_map = {}, {}
        for days, rating, uncertainty in whr.ratings_for_player(player):

            game_date = datetime.datetime(
                1941, 5, 18) + datetime.timedelta(days=days)
            rating_map[game_date.strftime("%Y-%m-%d")] = rating
            uncertainty_map[game_date.strftime("%Y-%m-%d")] = uncertainty

        winner_df['WWHR'] = winner_df['date'].map(rating_map).shift()
        winner_df['WWHR-Error'] = winner_df['date'].map(
            uncertainty_map).shift()

        loser_df['LWHR'] = loser_df['date'].map(rating_map).shift()
        loser_df['LWHR-Error'] = loser_df['date'].map(uncertainty_map).shift()

        games_df.update(winner_df)
        games_df.update(loser_df)

    games_df.to_csv("../../data/processed/v3.csv", index=False)
