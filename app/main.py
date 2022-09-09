from fastapi import FastAPI

from app.api import add_score, get_games, get_players, get_scores

app = FastAPI()


for module in [add_score, get_games, get_players, get_scores]:
    app.include_router(module.router)
