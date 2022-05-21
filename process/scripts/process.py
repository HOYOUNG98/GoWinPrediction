from os import listdir
import pandas as pd
from sgfmill.sgf import Sgf_game
from tqdm import tqdm


if __name__ == "__main__":
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
                'player': game.get_player_name(winner),
                'opponent': game.get_player_name(loser),
                'player_color': winner,
                'opponent_color': loser,
                'date': game.get_root().get('DT'),
                'player_rank': game.get_root().get(f'{winner.upper()}R'),
                'player_rank': game.get_root().get(f'{loser.upper()}R'),
                'komi': game.get_root().get('KM')
            })

    games_df = pd.DataFrame(games)
    games_df.to_csv("../data/processed/data.csv", index=False)
