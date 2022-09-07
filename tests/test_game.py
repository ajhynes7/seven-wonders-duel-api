import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.game import Game
from app.models.player import Player


@pytest.mark.parametrize("date", ["2022-09-01", "2022-09-02"])
def test_game(session: Session, client: TestClient, date: str):

    game = Game(date=date)
    session.add(game)

    response = client.get("/games")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "date": date},
    ]


def test_multiple_games(session: Session, client: TestClient):

    dates = ["2022-01-01", "2022-01-02", "2022-01-03"]

    for date in dates:
        game = Game(date=date)
        session.add(game)

    response = client.get("/games")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "date": dates[0]},
        {"id": 2, "date": dates[1]},
        {"id": 3, "date": dates[2]},
    ]
