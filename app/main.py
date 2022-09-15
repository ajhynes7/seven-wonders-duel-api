from fastapi import FastAPI

from app.api import (
    add_game,
    add_military_win,
    add_score,
    get_games,
    get_players,
    get_scores,
    get_wins,
)

app = FastAPI()


for module in [
    add_game,
    add_military_win,
    add_score,
    get_games,
    get_players,
    get_scores,
    get_wins,
]:
    app.include_router(module.router)
