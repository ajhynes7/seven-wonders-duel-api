import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models.game import Game


@pytest.mark.parametrize("date", ["2022-09-01", "2022-09-02"])
def test_get_game(session: Session, client: TestClient, date: str):

    game = Game(date=date)
    session.add(game)

    response = client.get("/games")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "date": date},
    ]


def test_get_games(session: Session, client: TestClient):

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


@pytest.mark.parametrize("date", ["2022-09-01", "2022-09-02", "2022-09-03"])
def test_add_game(session: Session, client: TestClient, date: str):

    response = client.post("/games", json={"date": date})

    assert response.status_code == 201
    assert response.json() == {"id": 1, "date": date}

    statement = select(Game).where(Game.id == 1)
    assert session.exec(statement).one()


@pytest.mark.parametrize("date", ["abc", "123", "2022", "2022-09", "2022-09-015"])
def test_add_invalid_game(session: Session, client: TestClient, date: str):

    response = client.post("/games", json={"date": date})

    assert response.status_code == 422

    response_json = response.json()
    assert (
        response_json["detail"][0]["msg"] == "The date must have the format YYYY-MM-DD."
    )

    statement = select(Game)
    assert not session.exec(statement).all()
