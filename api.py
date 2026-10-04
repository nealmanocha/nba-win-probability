import os

from fastapi import FastAPI
from train_model import train

import redis
r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model, feature_cols = train()

@app.get("/")
def read_root():
    return {"message": "NBA Win Probability API is running"}

@app.get("/predict")
def predict(fg_pct_home: float, fg_pct_away: float,
            ft_pct_home: float, ft_pct_away: float,
            fg3_pct_home: float, fg3_pct_away: float,
            ast_home: float, ast_away: float,
            reb_home: float, reb_away: float,
            tov_home: float, tov_away: float):

    cache_key = f"predict:{fg_pct_home}:{fg_pct_away}:{ft_pct_home}:{ft_pct_away}:{fg3_pct_home}:{fg3_pct_away}:{ast_home}:{ast_away}:{reb_home}:{reb_away}:{tov_home}:{tov_away}"

    cached_value = r.get(cache_key)
    if cached_value is not None:
        return {"home_win_probability": float(cached_value), "cached": True}

    input_data = [[fg_pct_home, fg_pct_away, ft_pct_home, ft_pct_away,
                   fg3_pct_home, fg3_pct_away, ast_home, ast_away,
                   reb_home, reb_away, tov_home, tov_away]]

    probability = model.predict_proba(input_data)[0][1]

    r.set(cache_key, str(probability), ex=60)

    return {"home_win_probability": probability, "cached": False}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)