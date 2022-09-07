from fastapi import Depends, FastAPI
from sqlmodel import Session, create_engine, select

from app.models.player import Player

app = FastAPI()
engine = create_engine("postgresql://localhost:5432/seven_wonders_duel")


def get_session():

    with Session(engine) as session:
        yield session


@app.get("/players")
def get_players(session: Session = Depends(get_session)):

    statement = select(Player)
    players = session.exec(statement).all()

    return players
