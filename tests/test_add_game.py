import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models.game import Game


@pytest.mark.parametrize("date", ["2022-09-01", "2022-09-02", "2022-09-03"])
def test_add_game(session: Session, client: TestClient, date: str):

    response = client.post("/games", json={"date": date})

    assert response.status_code == 201
    assert response.json() == {"id": 1, "date": date}

    statement = select(Game).where(Game.id == 1)
    assert session.exec(statement).one()
