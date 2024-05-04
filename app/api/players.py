from fastapi import Depends
from fastapi.routing import APIRouter
from sqlmodel import Session, select

from app.api.util import get_session
from app.models.player import Player

router = APIRouter()


@router.get("/players")
def get_players(session: Session = Depends(get_session)):
    statement = select(Player)
    players = session.exec(statement).all()

    return players
