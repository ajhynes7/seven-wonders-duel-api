import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.player import Player


@pytest.mark.parametrize("name", ["Andrew", "Alice"])
def test_get_player(session: Session, client: TestClient, name: str):

    player = Player(name=name)
    session.add(player)

    response = client.get("/players")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": name},
    ]


def test_get_players(session: Session, client: TestClient):

    names = ["Andrew", "Alice"]

    for name in names:
        session.add(Player(name=name))

    response = client.get("/players")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": names[0]},
        {"id": 2, "name": names[1]},
    ]
