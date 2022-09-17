import pytest
from fastapi.testclient import TestClient
from sqlmodel.orm.session import Session
from sqlmodel.sql.expression import select

from app.models.game import Game
from app.models.military_supremacy import MilitarySupremacy
from app.models.player import Player


def test_get_military_supremacy(
    session: Session, client: TestClient, games: list[Game], players: list[Player]
):
    military = MilitarySupremacy(game_id=games[0].id, player_id=players[0].id)

    session.add(military)
    session.commit()

    response = client.get("/military-supremacies")

    assert response.status_code == 200
    assert response.json() == [
        {"game_id": games[0].id, "game_date": games[0].date, "winner": players[0].name},
    ]


@pytest.mark.usefixtures("scores")
def test_add_military_supremacy(
    session: Session, client: TestClient, games: list[Game], players: list[Player]
):
    response = client.post(
        "/military-supremacies",
        json={"game_id": games[0].id, "player_id": players[0].id},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "game_id": games[0].id,
        "player_id": players[0].id,
    }

    statement = select(MilitarySupremacy).where(MilitarySupremacy.id == 1)
    military_supremacy = session.exec(statement).one()

    assert military_supremacy.game_id == games[0].id
    assert military_supremacy.player_id == players[0].id
