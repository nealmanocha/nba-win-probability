import sqlite3

DB_NAME = "nba_games.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            game_id TEXT PRIMARY KEY,
            game_date TEXT,
            arena_name TEXT,
            status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_game_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id TEXT REFERENCES games(game_id),
            team_abbr TEXT,
            points INTEGER,
            fg_pct REAL,
            ft_pct REAL,
            fg3_pct REAL,
            ast INTEGER,
            reb INTEGER,
            tov INTEGER,
            UNIQUE(game_id, team_abbr)
        )
    """)

    conn.commit()
    conn.close()

def insert_game(game_id, game_date, arena_name, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO games (game_id, game_date, arena_name, status)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(game_id) DO UPDATE SET
            game_date = excluded.game_date,
            arena_name = excluded.arena_name,
            status = excluded.status
    """, (game_id, game_date, arena_name, status))

    conn.commit()
    conn.close()

def insert_team_stats(game_id, team_abbr, points, fg_pct, ft_pct, fg3_pct, ast, reb, tov):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO team_game_stats (game_id, team_abbr, points, fg_pct, ft_pct, fg3_pct, ast, reb, tov)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(game_id, team_abbr) DO UPDATE SET
            points = excluded.points,
            fg_pct = excluded.fg_pct,
            ft_pct = excluded.ft_pct,
            fg3_pct = excluded.fg3_pct,
            ast = excluded.ast,
            reb = excluded.reb,
            tov = excluded.tov
    """, (game_id, team_abbr, points, fg_pct, ft_pct, fg3_pct, ast, reb, tov))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Tables created.")