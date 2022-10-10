from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from sqlmodel import Session, select

from app.api.util import get_session
from app.models.game import Game
from app.models.player import Player
from app.models.supremacy import Supremacy

router = APIRouter()


@router.get("/supremacies")
def get_supremacies(
    session: Session = Depends(get_session),
):
    statement = (
        select(
            Supremacy.game_id,
            Game.date.label("game_date"),
            Supremacy.type,
            Player.name.label("winner"),
        )
        .join(Game, Supremacy.game_id == Game.id)
        .join(Player, Supremacy.player_id == Player.id)
    )

    winners = session.exec(statement).all()

    return winners


@router.post("/supremacies", status_code=201)
def add_supremacy(supremacy: Supremacy, session: Session = Depends(get_session)):
    session.add(supremacy)

    try:
        session.commit()
    except Exception:
        raise HTTPException(status_code=403)

    session.refresh(supremacy)

    return supremacy
