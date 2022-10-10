import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.game import Game
from app.models.player import Player
from app.models.supremacy import Supremacy


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
def test_get_wins_with_supremacies(
    session: Session, client: TestClient, games: list[Game], players: list[Player]
):

    for date in ["2022-09-17", "2022-09-18"]:
        game = Game(date=date)
        games.append(game)

        session.add(game)

    session.commit()

    military_supremacy = Supremacy(
        game_id=games[3].id, player_id=players[0].id, type="military"
    )
    scientific_supremacy = Supremacy(
        game_id=games[4].id, player_id=players[1].id, type="scientific"
    )

    session.add_all([military_supremacy, scientific_supremacy])
    session.commit()

    response = client.get("/wins")

    assert response.status_code == 200

    assert response.json() == [
        {"game_id": games[0].id, "game_date": games[0].date, "winner": players[1].name},
        {"game_id": games[1].id, "game_date": games[1].date, "winner": players[0].name},
        {"game_id": games[2].id, "game_date": games[2].date, "winner": players[0].name},
        {"game_id": games[3].id, "game_date": games[3].date, "winner": players[0].name},
        {"game_id": games[4].id, "game_date": games[4].date, "winner": players[1].name},
    ]


@pytest.mark.usefixtures("scores")
def test_get_win_of_game(client: TestClient, games: list[Game], players: list[Player]):

    response = client.get("/wins", params={"game_id": 1})

    assert response.status_code == 200

    assert response.json() == [
        {
            "game_id": games[0].id,
            "game_date": games[0].date,
            "winner": players[1].name,
        }
    ]


@pytest.mark.usefixtures("scores", "games")
def test_get_total_wins(client: TestClient, players: list[Player]):

    response = client.get("/wins/total")

    assert response.status_code == 200

    assert response.json() == [
        {"player_name": players[0].name, "total_wins": 2},
        {"player_name": players[1].name, "total_wins": 1},
    ]
