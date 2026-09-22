# nba-win-probability
# NBA Win Probability Pipeline

An end-to-end data pipeline that ingests NBA game data, stores it in a relational database, engineers model-ready features, and trains a simple win-probability model — built to learn system design fundamentals (APIs, databases, data pipelines) alongside applied ML.

## What it does

1. **Ingestion** (`ingest.py`) — pulls game and team box score data from the NBA Stats API (`nba_api`), supporting both a specific historical date and (once the season is live) real-time polling.
2. **Storage** (`db.py`) — persists data into a normalized SQLite schema: a `games` table (one row per game) and a `team_game_stats` table (one row per team per game), linked by `game_id`. Inserts are idempotent (upsert-based), so repeated polling of the same game safely updates rather than duplicates.
3. **Feature engineering** (`features.py`) — joins home and away team stats into a single row per game, producing a model-ready table with a `home_win` label.
4. **Backfill** (`backfill.py`) — loops the ingestion pipeline over multiple historical dates to grow the training dataset.
5. **Model training** (`train_model.py`) — trains a logistic regression model to predict `home_win` from team performance stats (shooting %, assists, rebounds, turnovers).

## Known limitation: dataset size

At this stage, the database contains a small number of backfilled dates (a few dozen games). With this little data, model accuracy is **not statistically meaningful** — repeated training runs on the same code show meaningfully different accuracy scores (observed range: ~55%-89%) purely due to which games randomly land in the train/test split.

This is an expected and understood limitation of the current dataset size, not a bug in the pipeline. The pipeline itself is fully functional and designed to scale: backfilling additional historical dates, or letting the ingestion pipeline run through a live season, would substantially grow the dataset and produce more reliable accuracy estimates.

## Tech stack

- Python, pandas, scikit-learn
- SQLite
- `nba_api` (NBA Stats API wrapper)

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python db.py            # create tables
python backfill.py      # populate historical data
python train_model.py   # train and evaluate the model
```
