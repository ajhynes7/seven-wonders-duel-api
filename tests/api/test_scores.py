import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from sqlmodel.sql.expression import select

from app.models.game import Game
from app.models.player import Player
from app.models.score import Score


def test_get_score(
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
            "game_id": games[0].id,
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


def test_get_scores_ordered_by_game_id_and_player_id(
    session: Session, client: TestClient, players: list[Player]
):
    game_date = "2022-10-09"

    for game_id in [2, 1]:
        game = Game(id=game_id, date=game_date)

        for player_index in [1, 0]:
            score = Score(
                game_id=game_id,
                player_id=players[player_index].id,
                civilian=1,
                science=1,
                commerce=1,
                guilds=1,
                wonders=1,
                tokens=1,
                coins=1,
                military=1,
            )

            session.add_all([game, score])

    session.commit()

    response = client.get("/scores")

    assert response.status_code == 200
    assert response.json() == [
        {
            "game_id": 1,
            "game_date": game_date,
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
            "game_id": 1,
            "game_date": game_date,
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
        {
            "game_id": 2,
            "game_date": game_date,
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
            "game_id": 2,
            "game_date": game_date,
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
def test_get_score_of_game(
    client: TestClient, games: list[Game], players: list[Player]
):
    response = client.get("/scores", params={"game_id": 1})

    assert response.status_code == 200
    assert response.json() == [
        {
            "game_id": games[0].id,
            "game_date": games[0].date,
            "player_name": players[0].name,
            "civilian": 28,
            "science": 0,
            "commerce": 6,
            "guilds": 8,
            "wonders": 9,
            "tokens": 0,
            "coins": 5,
            "military": 2,
        },
        {
            "game_id": games[0].id,
            "game_date": games[0].date,
            "player_name": players[1].name,
            "civilian": 16,
            "science": 6,
            "commerce": 6,
            "guilds": 6,
            "wonders": 21,
            "tokens": 0,
            "coins": 4,
            "military": 0,
        },
    ]


@pytest.mark.usefixtures("scores")
def test_get_total_scores(client: TestClient, games: list[Game], players: list[Player]):
    response = client.get("/scores/total")

    assert response.status_code == 200
    assert response.json() == [
        {
            "game_id": games[0].id,
            "game_date": games[0].date,
            "player_name": players[0].name,
            "total": 58,
        },
        {
            "game_id": games[0].id,
            "game_date": games[0].date,
            "player_name": players[1].name,
            "total": 59,
        },
        {
            "game_id": games[1].id,
            "game_date": games[1].date,
            "player_name": players[0].name,
            "total": 64,
        },
        {
            "game_id": games[1].id,
            "game_date": games[1].date,
            "player_name": players[1].name,
            "total": 49,
        },
        {
            "game_id": games[2].id,
            "game_date": games[2].date,
            "player_name": players[0].name,
            "total": 59,
        },
        {
            "game_id": games[2].id,
            "game_date": games[2].date,
            "player_name": players[1].name,
            "total": 55,
        },
    ]


@pytest.mark.usefixtures("scores")
def test_get_total_scores_of_game(
    client: TestClient, games: list[Game], players: list[Player]
):
    response = client.get("/scores/total", params={"game_id": 1})

    assert response.status_code == 200
    assert response.json() == [
        {
            "game_id": games[0].id,
            "game_date": games[0].date,
            "player_name": players[0].name,
            "total": 58,
        },
        {
            "game_id": games[0].id,
            "game_date": games[0].date,
            "player_name": players[1].name,
            "total": 59,
        },
    ]


def test_add_score(
    session: Session, client: TestClient, games: list[Game], players: list[Player]
):
    post_json = {
        "game_id": games[0].id,
        "player_id": players[0].id,
        "civilian": 1,
        "science": 1,
        "commerce": 1,
        "guilds": 1,
        "wonders": 1,
        "tokens": 1,
        "coins": 1,
        "military": 1,
    }

    response = client.post("/scores", json=post_json)

    assert response.status_code == 201

    response_json = response.json()
    assert response_json == post_json

    statement = select(Score).where(Game.id == games[0].id, Player.id == players[0].id)
    assert session.exec(statement).one()


def test_add_score_with_invalid_game(client: TestClient, players: list[Player]):
    response = client.post(
        "/scores",
        json={
            "game_id": 1,
            "player_id": players[0].id,
            "civilian": 1,
            "science": 1,
            "commerce": 1,
            "guilds": 1,
            "wonders": 1,
            "tokens": 1,
            "coins": 1,
            "military": 1,
        },
    )

    assert response.status_code == 403


def test_add_score_with_invalid_player(client: TestClient, games: list[Game]):
    response = client.post(
        "/scores",
        json={
            "game_id": games[0].id,
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
    )

    assert response.status_code == 403
