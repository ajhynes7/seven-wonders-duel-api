import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.game import Game
from app.models.player import Player
from app.models.score import Score


def test_score(session: Session, client: TestClient):

    score = Score(
        game_id=1,
        player_id=1,
        civilian=1,
        science=1,
        commerce=1,
        guilds=1,
        wonders=1,
        tokens=1,
        coins=1,
        military=1,
    )
    session.add(score)

    response = client.get("/scores")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "game_id": 1,
            "player_id": 1,
            "civilian": 1,
            "science": 1,
            "commerce": 1,
            "guilds": 1,
            "wonders": 1,
            "tokens": 1,
            "coins": 1,
            "military": 1,
        },
    ]
