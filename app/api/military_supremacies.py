from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from sqlmodel import Session, select

from app.api.util import get_session
from app.models.game import Game
from app.models.military_supremacy import MilitarySupremacy
from app.models.player import Player

router = APIRouter()


@router.get("/military-supremacies")
def get_military_supremacies(
    session: Session = Depends(get_session),
):

    statement = (
        select(
            MilitarySupremacy.game_id,
            Game.date.label("game_date"),
            Player.name.label("winner"),
        )
        .join(Game, MilitarySupremacy.game_id == Game.id)
        .join(Player, MilitarySupremacy.player_id == Player.id)
    )

    winners = session.exec(statement).all()

    return winners


@router.post("/military-supremacies", status_code=201)
def add_military_win(
    military_supremacy: MilitarySupremacy, session: Session = Depends(get_session)
):

    session.add(military_supremacy)

    try:
        session.commit()
    except Exception:
        raise HTTPException(status_code=403)

    session.refresh(military_supremacy)

    return military_supremacy
