# NBA Win Probability Pipeline

An end-to-end system that ingests NBA game data, stores it in a relational database, engineers model-ready features, trains a logistic regression model, and serves predictions through a cached API with a simple dashboard. Everything runs in Docker.

I built it to learn system design by building a real system, and to practice making and explaining tradeoffs at each layer.

## Architecture

    NBA Stats API
         |
    ingest.py / backfill.py   (fetch game and team box scores)
         |
    SQLite (db.py)            (games, team_game_stats)
         |
    features.py               (one row per game, home_win label)
         |
    train_model.py            (logistic regression)
         |
    FastAPI (api.py)  <---->  Redis (60s cache)
         |
    dashboard.html            (calls /predict)

## Design decisions and tradeoffs

- **Normalized schema.** Two tables (`games`, `team_game_stats`) linked by `game_id`, instead of one wide row per game. Querying all games for a team is one simple filter, and game-level facts are not duplicated. The cost is a join when building features.
- **Idempotent writes.** Inserts are upserts (`ON CONFLICT ... DO UPDATE`), so polling the same game repeatedly updates it instead of crashing or duplicating rows. Team rows are unique on `(game_id, team_abbr)`.
- **Separation of concerns.** Fetching, storage, features, training, and serving are separate modules. Swapping SQLite for Postgres would only touch `db.py`.
- **SQLite over Postgres.** No server to run and enough for this data volume. I would switch once there are concurrent writers.
- **Redis cache with a 60 second TTL.** Identical requests skip the model. The TTL is a freshness versus speed tradeoff, chosen because live game stats change quickly.
- **Docker Compose.** The API and Redis run as two containers on a shared network, with the Redis host set by an environment variable so the same code runs locally and in containers.
- **Parameterized SQL.** All queries use placeholders, never string formatting, to avoid SQL injection.

## Known limitations

- **Small dataset.** The database holds roughly 44 games from 6 backfilled dates. Repeated training runs on the same code gave accuracy anywhere from about 55% to 89%, driven by which games land in the test split. These numbers are not statistically meaningful yet. The pipeline is built to scale with more backfilled dates or a live season.
- **The features are not pre-game information.** The model uses final box score stats from the game being predicted, so it describes what a winning stat line looks like. A true win-probability model would use pre-game or in-progress state (team form, rest days, score and time remaining). I removed the raw points columns after seeing they leaked the label (100% accuracy), but the underlying issue remains.
- **The model retrains on every API start.** The split is random, so predictions shift slightly between restarts. The fix is to train once, save the model to a file, and load it in the API.
- **No live polling yet.** The ingestion code supports polling, but the season was not active during development, so I built and tested against historical dates.
- **Exact-match cache keys.** Two requests that differ by a tiny float rounding get separate cache entries.
- **The dashboard is not containerized.** It is a static HTML file that calls the API on `localhost:8000`.
- **The API uses GET with 12 query parameters.** A POST with a JSON body is the more conventional design.

## Run it

Build the data first (once), then start the stack:

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python db.py             # create tables
    python backfill.py       # fetch historical games
    docker compose up --build

Then open `dashboard.html` in a browser and click "Get Prediction". API docs are at `http://localhost:8000/docs`.

## Tech stack

Python, pandas, scikit-learn, SQLite, FastAPI, Redis, Docker, `nba_api`.

## What I would do next

1. Save the trained model and load it at startup.
2. Backfill a full season and use proper cross-validation.
3. Replace the features with pre-game information.
4. Serve the dashboard from the API or an nginx container.
5. Poll live games and write predictions back to the database.