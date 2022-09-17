from fastapi import FastAPI

from app.api import games, military_supremacies, players, scores, wins

app = FastAPI()


for module in [
    games,
    military_supremacies,
    players,
    scores,
    wins,
]:
    app.include_router(module.router)
