import time
from nba_api.stats.endpoints import scoreboardv2

def get_live_games():
    board = scoreboardv2.ScoreboardV2(game_date='2025-01-15')
    line_score = board.get_data_frames()[1]
    games = line_score[['GAME_ID', 'TEAM_ABBREVIATION', 'PTS']]
    return games

def poll_games(interval_seconds=30, max_polls=5):
    # TODO: loop max_polls times
    # each loop: call get_live_games(), print result
    # then time.sleep(interval_seconds)
    for i in range(max_polls):
        live_games = get_live_games()
        print(live_games)
        time.sleep(interval_seconds)

if __name__ == "__main__":
    poll_games()