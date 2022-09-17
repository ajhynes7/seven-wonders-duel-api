import pytest
from fastapi.testclient import TestClient
from sqlmodel.orm.session import Session
from sqlmodel.sql.expression import select

from app.models.game import Game
from app.models.player import Player
from app.models.scientific_supremacy import ScientificSupremacy


def test_get_scientific_supremacy(
    session: Session, client: TestClient, games: list[Game], players: list[Player]
):
    scientific = ScientificSupremacy(game_id=games[0].id, player_id=players[0].id)

    session.add(scientific)
    session.commit()

    response = client.get("/scientific-supremacies")

    assert response.status_code == 200
    assert response.json() == [
        {"game_id": games[0].id, "game_date": games[0].date, "winner": players[0].name},
    ]


@pytest.mark.usefixtures("scores")
def test_add_scientific_supremacy(
    session: Session, client: TestClient, games: list[Game], players: list[Player]
):
    response = client.post(
        "/scientific-supremacies",
        json={"game_id": games[0].id, "player_id": players[0].id},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "game_id": games[0].id,
        "player_id": players[0].id,
    }

    statement = select(ScientificSupremacy).where(ScientificSupremacy.id == 1)
    scientific_supremacy = session.exec(statement).one()

    assert scientific_supremacy.game_id == games[0].id
    assert scientific_supremacy.player_id == players[0].id
