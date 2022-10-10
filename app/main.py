from fastapi import FastAPI

from app.api import games, players, scores, supremacies, wins

app = FastAPI()


for module in [
    games,
    players,
    scores,
    supremacies,
    wins,
]:
    app.include_router(module.router)
