from fastapi.testclient import TestClient
from sqlmodel.orm.session import Session

from app.models.game import Game
from app.models.military_supremacy import MilitarySupremacy
from app.models.player import Player


def test_get_military_wins(
    session: Session, client: TestClient, games: list[Game], players: list[Player]
):
    military = MilitarySupremacy(game_id=games[0].id, player_id=players[0].id)

    session.add(military)
    session.commit()

    response = client.get("/wins/military")

    assert response.status_code == 200

    assert response.json() == [
        {"game_id": games[0].id, "game_date": games[0].date, "winner": players[0].name},
    ]
