import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.game import Game
from app.models.player import Player
from app.models.score import Score
from app.models.supremacy import Supremacy


@pytest.mark.usefixtures("scores")
def test_get_wins(client: TestClient, games: list[Game], players: list[Player]):
    response = client.get("/wins")

    assert response.status_code == 200

    assert response.json() == [
        {
            "game_id": games[0].id,
            "player_id": 2,
        },
        {
            "game_id": games[1].id,
            "player_id": 1,
        },
        {
            "game_id": games[2].id,
            "player_id": 1,
        },
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
        {
            "game_id": games[0].id,
            "player_id": 2,
        },
        {
            "game_id": games[1].id,
            "player_id": 1,
        },
        {
            "game_id": games[2].id,
            "player_id": 1,
        },
        {
            "game_id": games[3].id,
            "player_id": 1,
        },
        {
            "game_id": games[4].id,
            "player_id": 2,
        },
    ]


@pytest.mark.usefixtures("scores")
def test_get_win_of_game(client: TestClient, games: list[Game]):
    response = client.get("/wins", params={"game_id": 1})

    assert response.status_code == 200

    assert response.json() == [
        {
            "game_id": games[0].id,
            "player_id": 2,
        }
    ]


@pytest.mark.usefixtures("scores")
def test_get_total_wins(client: TestClient):
    response = client.get("/wins/total")

    assert response.status_code == 200

    assert response.json() == [
        {"player_id": 1, "count": 2},
        {"player_id": 2, "count": 1},
    ]


@pytest.mark.usefixtures("scores")
def test_get_total_wins_with_tie(client: TestClient, session: Session):
    game = Game(date="2024-05-28")
    session.add(game)
    session.commit()

    for player_id in [1, 2]:
        score = Score(
            game_id=game.id,
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
        session.add(score)

    session.commit()

    response = client.get("/wins/total")

    assert response.status_code == 200

    assert response.json() == [
        {"player_id": 0, "count": 1},
        {"player_id": 1, "count": 2},
        {"player_id": 2, "count": 1},
    ]
