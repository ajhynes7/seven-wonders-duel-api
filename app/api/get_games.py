from fastapi import Depends
from fastapi.routing import APIRouter
from sqlmodel import Session, select

from app.api.util import get_session
from app.models.game import Game

router = APIRouter()


@router.get("/games")
def get_games(session: Session = Depends(get_session)):

    statement = select(Game)
    games = session.exec(statement).all()

    return games
