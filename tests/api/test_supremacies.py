import pytest
from fastapi.testclient import TestClient
from sqlmodel.orm.session import Session
from sqlmodel.sql.expression import select

from app.models.game import Game
from app.models.player import Player
from app.models.supremacy import Supremacy


@pytest.mark.parametrize("supremacy_type", ["military", "scientific"])
def test_get_supremacy(
    session: Session,
    client: TestClient,
    games: list[Game],
    players: list[Player],
    supremacy_type: str,
):
    supremacy = Supremacy(
        game_id=games[0].id, player_id=players[0].id, type=supremacy_type
    )

    session.add(supremacy)
    session.commit()

    response = client.get("/supremacies")

    assert response.status_code == 200
    assert response.json() == [
        {
            "game_id": games[0].id,
            "game_date": games[0].date,
            "player_name": players[0].name,
            "type": supremacy_type,
        },
    ]


def test_get_supremacies_ordered_by_game_id(
    session: Session, client: TestClient, players: list[Player]
):
    game_date = "2022-10-09"

    for game_id, player_index, supremacy_type in zip(
        [3, 2, 1, 4], [0, 0, 1, 0], ["military", "military", "scientific", "scientific"]
    ):
        game = Game(id=game_id, date=game_date)

        supremacy = Supremacy(
            game_id=game.id,
            player_id=players[player_index].id,
            type=supremacy_type,
        )

        session.add_all([game, supremacy])

    session.commit()

    response = client.get("/supremacies")

    assert response.status_code == 200

    assert response.json() == [
        {
            "game_id": 1,
            "game_date": game_date,
            "player_name": players[1].name,
            "type": "scientific",
        },
        {
            "game_id": 2,
            "game_date": game_date,
            "player_name": players[0].name,
            "type": "military",
        },
        {
            "game_id": 3,
            "game_date": game_date,
            "player_name": players[0].name,
            "type": "military",
        },
        {
            "game_id": 4,
            "game_date": game_date,
            "player_name": players[0].name,
            "type": "scientific",
        },
    ]


@pytest.mark.usefixtures("scores")
@pytest.mark.parametrize("supremacy_type", ["military", "scientific"])
def test_add_supremacy(
    session: Session,
    client: TestClient,
    games: list[Game],
    players: list[Player],
    supremacy_type: str,
):
    response = client.post(
        "/supremacies",
        json={
            "game_id": games[0].id,
            "player_id": players[0].id,
            "type": supremacy_type,
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "game_id": games[0].id,
        "player_id": players[0].id,
        "type": supremacy_type,
    }

    statement = select(Supremacy).where(Supremacy.game_id == games[0].id)
    supremacy = session.exec(statement).one()

    assert supremacy.game_id == games[0].id
    assert supremacy.player_id == players[0].id


@pytest.mark.parametrize("supremacy_type", ["military", "scientific"])
def test_add_supremacy_with_invalid_game(
    client: TestClient, players: list[Player], supremacy_type: str
):
    response = client.post(
        "/supremacies",
        json={"game_id": 1, "player_id": players[0].id, "type": supremacy_type},
    )

    assert response.status_code == 403


@pytest.mark.parametrize("supremacy_type", ["military", "scientific"])
def test_add_supremacy_with_invalid_player(
    client: TestClient, games: list[Game], supremacy_type
):
    response = client.post(
        "/supremacies",
        json={"game_id": games[0].id, "player_id": 1, "type": supremacy_type},
    )

    assert response.status_code == 403


@pytest.mark.parametrize("supremacy_type", ["military", "scientific"])
def test_add_supremacy_with_duplicate_game(
    client: TestClient, games: list[Game], players: list[Player], supremacy_type: str
):
    response = client.post(
        "/supremacies",
        json={
            "game_id": games[0].id,
            "player_id": players[0].id,
            "type": supremacy_type,
        },
    )

    assert response.status_code == 201

    response = client.post(
        "/supremacies",
        json={
            "game_id": games[0].id,
            "player_id": players[0].id,
            "type": supremacy_type,
        },
    )

    assert response.status_code == 403


@pytest.mark.parametrize("supremacy_type", ["foo", "bar", "militar", "scientifi"])
def test_add_supremacy_with_invalid_type(
    client: TestClient, games: list[Game], players: list[Player], supremacy_type: str
):
    response = client.post(
        "/supremacies",
        json={
            "game_id": games[0].id,
            "player_id": players[0].id,
            "type": supremacy_type,
        },
    )

    assert response.status_code == 422
