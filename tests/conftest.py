import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app, get_session
from app.models.game import Game
from app.models.player import Player
from app.models.score import Score


@pytest.fixture()
def session():

    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Enable foreign key constraints in the SQLite test database.
        session.execute("pragma foreign_keys=on")

        yield session


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

    games = [Game(date=date) for date in ["2022-09-01", "2022-01-02", "2022-09-03"]]

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

    scores = [
        Score(
            game_id=game.id,
            player_id=player.id,
            civilian=1,
            science=1,
            commerce=1,
            guilds=1,
            wonders=1,
            tokens=1,
            coins=1,
            military=1,
        )
        for game in games
        for player in players
    ]

    session.add_all(scores)
    session.commit()

    return scores
