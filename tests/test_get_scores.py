import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.game import Game
from app.models.player import Player
from app.models.score import Score


def test_score(
    session: Session, client: TestClient, games: list[Game], players: list[Player]
):

    score = Score(
        game_id=games[0].id,
        player_id=players[0].id,
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

    response = client.get("/scores")

    assert response.status_code == 200
    assert response.json() == [
        {
            "game_date": games[0].date,
            "player_name": players[0].name,
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


@pytest.mark.usefixtures("scores")
def test_get_score_of_game(
    client: TestClient, games: list[Game], players: list[Player]
):

    response = client.get("/scores", params={"game_id": 1})

    assert response.status_code == 200
    assert response.json() == [
        {
            "game_date": games[0].date,
            "player_name": players[0].name,
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
            "game_date": games[0].date,
            "player_name": players[1].name,
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


@pytest.mark.usefixtures("scores")
def test_total_scores(client: TestClient, games: list[Game], players: list[Player]):

    response = client.get("/scores/total")

    assert response.status_code == 200
    assert response.json() == [
        {"game_date": games[0].date, "player_name": players[0].name, "total": 8},
        {"game_date": games[0].date, "player_name": players[1].name, "total": 8},
        {"game_date": games[1].date, "player_name": players[0].name, "total": 8},
        {"game_date": games[1].date, "player_name": players[1].name, "total": 8},
        {"game_date": games[2].date, "player_name": players[0].name, "total": 8},
        {"game_date": games[2].date, "player_name": players[1].name, "total": 8},
    ]


@pytest.mark.usefixtures("scores")
def test_total_scores_of_game(
    client: TestClient, games: list[Game], players: list[Player]
):

    response = client.get("/scores/total", params={"game_id": 1})

    assert response.status_code == 200
    assert response.json() == [
        {"game_date": games[0].date, "player_name": players[0].name, "total": 8},
        {"game_date": games[0].date, "player_name": players[1].name, "total": 8},
    ]
