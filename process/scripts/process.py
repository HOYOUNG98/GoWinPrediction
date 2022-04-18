from os import listdir
import pandas as pd
from sgfmill.sgf import Sgf_game
from tqdm import tqdm

files = listdir("../data/raw")
games = []
for file in tqdm(files):
    file = "".join(["../data/raw/", file])
    with open(file, "rb") as f:
        game = Sgf_game.from_bytes(f.read())
        winner = game.get_winner()
        loser = 'w' if winner == 'b' else 'b'

        if not winner:
            continue

        games.append({
            'win_name': game.get_player_name(winner),
            'lose_name': game.get_player_name(loser),
            'win_color': winner,
            'lose_color': loser,
            'date': game.get_root().get('DT'),
            'win_rank': game.get_root().get(f'{winner.upper()}R'),
            'lose_rank': game.get_root().get(f'{loser.upper()}R'),
            'komi': game.get_root().get('KM')
        })

games_df = pd.DataFrame(games)
games_df.to_csv("../data/processed/data.csv", index=False)
