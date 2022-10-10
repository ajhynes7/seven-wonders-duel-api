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
            "winner": players[0].name,
            "type": supremacy_type,
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
