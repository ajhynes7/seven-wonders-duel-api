import pandas as pd
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.api.util import get_session
from app.main import app
from app.models.game import Game
from app.models.player import Player
from app.models.score import Score


@pytest.fixture()
def session():
    engine = create_engine(
        "postgresql://localhost:5432/seven_wonders_duel_test",
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    SQLModel.metadata.drop_all(engine)


@pytest.fixture()
def client(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def games(session: Session) -> list[Game]:
    games = [Game(date=date) for date in ["2022-09-01", "2022-09-02", "2022-09-03"]]

    session.add_all(games)
    session.commit()

    return games


@pytest.fixture()
def players(session: Session) -> list[Player]:
    players = [Player(name=name) for name in ["Andrew", "Alice"]]

    session.add_all(players)
    session.commit()

    return players


@pytest.fixture()
def scores(session: Session, games: list[Game], players: list[Player]) -> list[Score]:
    df_scores = pd.read_csv("tests/data/scores.csv")

    scores = []

    for _, row in df_scores.iterrows():
        score = Score(**row)
        scores.append(score)

    session.add_all(scores)
    session.commit()

    return scores
