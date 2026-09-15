import sqlite3
import pandas as pd

DB_NAME = "nba_games.db"

def build_features():
    conn = sqlite3.connect(DB_NAME)

    games = pd.read_sql_query("SELECT * FROM games", conn)
    stats = pd.read_sql_query("SELECT * FROM team_game_stats", conn)

    conn.close()

    merged = stats.merge(games, on='game_id')
    home_stats = merged[merged['team_id'] == merged['home_team_id']]
    away_stats = merged[merged['team_id'] == merged['visitor_team_id']]

    game_features = home_stats.merge(away_stats, on='game_id', suffixes=('_home', '_away'))
    game_features['home_win'] = (game_features['points_home'] > game_features['points_away']).astype(int)

    final_columns = [
        'game_id', 'game_date_home', 'arena_name_home',
        'team_abbr_home', 'team_abbr_away',
        'points_home', 'points_away',
        'fg_pct_home', 'fg_pct_away',
        'ft_pct_home', 'ft_pct_away',
        'fg3_pct_home', 'fg3_pct_away',
        'ast_home', 'ast_away',
        'reb_home', 'reb_away',
        'tov_home', 'tov_away',
        'home_win'
    ]
    game_features = game_features[final_columns]

    return game_features

if __name__ == "__main__":
    result = build_features()
    print(result)