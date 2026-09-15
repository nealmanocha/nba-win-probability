import time
from ingest import get_live_games
import db

dates_to_backfill = [
    '2025-01-10',
    '2025-01-11',
    '2025-01-12',
    '2025-01-13',
    '2025-01-14',
    '2025-01-15',
]

def backfill():
    for game_date in dates_to_backfill:
        print(f"Fetching {game_date}...")
        games_df, teams_df = get_live_games(game_date)

        for index, row in games_df.iterrows():
            db.insert_game(row['GAME_ID'], row['GAME_DATE_EST'], row['ARENA_NAME'], row['GAME_STATUS_TEXT'], row['HOME_TEAM_ID'], row['VISITOR_TEAM_ID'])

        for index, row in teams_df.iterrows():
            db.insert_team_stats(row['GAME_ID'], row['TEAM_ABBREVIATION'], row['PTS'], row['FG_PCT'], row['FT_PCT'], row['FG3_PCT'], row['AST'], row['REB'], row['TOV'], row['TEAM_ID'])

        time.sleep(1)

if __name__ == "__main__":
    backfill()