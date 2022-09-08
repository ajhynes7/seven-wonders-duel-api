from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models.score import Score


def test_add_score(session: Session, client: TestClient):

    response = client.post(
        "/scores",
        json={
            "game_id": 1,
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

    assert response.status_code == 201

    response_json = response.json()

    score_id = response_json["id"]
    assert score_id == 1

    statement = select(Score).where(Score.id == score_id)
    assert session.exec(statement).one()
