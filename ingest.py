import db
import time
from nba_api.stats.endpoints import scoreboardv2

def get_live_games():
    board = scoreboardv2.ScoreboardV2(game_date='2025-01-15')
    line_score = board.get_data_frames()[1]
    game_header = board.get_data_frames()[0]
    games_df = game_header[['GAME_ID', 'GAME_DATE_EST', 'ARENA_NAME', 'GAME_STATUS_TEXT']]
    teams_df = line_score[['GAME_ID', 'TEAM_ABBREVIATION', 'PTS', 'FG_PCT', 'FT_PCT', 'FG3_PCT', 'AST', 'REB', 'TOV']]
    return games_df, teams_df

def poll_games(interval_seconds=30, max_polls=5):
    for i in range(max_polls):
        games_df, teams_df = get_live_games()

        for index, row in games_df.iterrows():
            db.insert_game(row['GAME_ID'], row['GAME_DATE_EST'], row['ARENA_NAME'], row['GAME_STATUS_TEXT'])

        for index, row in teams_df.iterrows():
            db.insert_team_stats(row['GAME_ID'], row['TEAM_ABBREVIATION'], row['PTS'], row['FG_PCT'], row['FT_PCT'], row['FG3_PCT'], row['AST'], row['REB'], row['TOV'])

        print(games_df)
        print(teams_df)
        time.sleep(interval_seconds)
    


if __name__ == "__main__":
    poll_games()