from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.util import get_session
from app.models.game import Game

router = APIRouter()


@router.post("/games", status_code=201)
def add_game(game: Game, session: Session = Depends(get_session)):

    session.add(game)
    session.commit()
    session.refresh(game)

    return game
