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


def test_get_score_of_game(session: Session, client: TestClient):

    scores = [
        Score(
            game_id=game_id,
            player_id=player_id,
            civilian=1,
            science=1,
            commerce=1,
            guilds=1,
            wonders=1,
            tokens=1,
            coins=1,
            military=1,
        )
        for game_id in range(1, 4)
        for player_id in range(1, 3)
    ]

    for score in scores:
        session.add(score)

    response = client.get("/scores", params={"gameId": 1})

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
        {
            "id": 2,
            "game_id": 1,
            "player_id": 2,
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
