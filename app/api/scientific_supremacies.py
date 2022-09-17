from fastapi import Depends
from fastapi.routing import APIRouter
from sqlmodel import Session, select

from app.api.util import get_session
from app.models.game import Game
from app.models.player import Player
from app.models.scientific_supremacy import ScientificSupremacy

router = APIRouter()


@router.get("/scientific-supremacies")
def get_scientific_supremacies(
    session: Session = Depends(get_session),
):

    statement = (
        select(
            ScientificSupremacy.game_id,
            Game.date.label("game_date"),
            Player.name.label("winner"),
        )
        .join(Game, ScientificSupremacy.game_id == Game.id)
        .join(Player, ScientificSupremacy.player_id == Player.id)
    )

    winners = session.exec(statement).all()

    return winners


@router.post("/scientific-supremacies", status_code=201)
def add_scientific_win(
    scientific_supremacy: ScientificSupremacy, session: Session = Depends(get_session)
):

    session.add(scientific_supremacy)
    session.commit()
    session.refresh(scientific_supremacy)

    return scientific_supremacy
