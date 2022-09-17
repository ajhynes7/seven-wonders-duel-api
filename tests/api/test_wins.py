import pytest
from fastapi.testclient import TestClient

from app.models.game import Game
from app.models.player import Player


@pytest.mark.usefixtures("scores")
def test_get_wins(client: TestClient, games: list[Game], players: list[Player]):

    response = client.get("/wins")

    assert response.status_code == 200

    assert response.json() == [
        {"game_id": games[0].id, "game_date": games[0].date, "winner": players[1].name},
        {"game_id": games[1].id, "game_date": games[1].date, "winner": players[0].name},
        {"game_id": games[2].id, "game_date": games[2].date, "winner": players[0].name},
    ]


@pytest.mark.usefixtures("scores")
def test_get_wins_of_game(client: TestClient, games: list[Game], players: list[Player]):

    response = client.get("/wins", params={"game_id": 1})

    assert response.status_code == 200

    assert response.json() == [
        {"game_id": games[0].id, "game_date": games[0].date, "winner": players[1].name}
    ]
