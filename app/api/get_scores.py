from fastapi import Depends
from fastapi.routing import APIRouter
from sqlmodel import Session, select

from app.api.util import get_session
from app.models.score import Score

router = APIRouter()


@router.get("/scores")
def get_scores(
    game_id: int | None = None,
    session: Session = Depends(get_session),
):

    statement = select(Score)

    if game_id:
        statement = statement.where(Score.game_id == game_id)

    scores = session.exec(statement).all()

    return scores


@router.get("/scores/total")
def get_total_scores(
    game_id: int | None = None,
    session: Session = Depends(get_session),
):

    statement = select(
        Score.game_id,
        Score.player_id,
        (
            Score.civilian
            + Score.science
            + Score.commerce
            + Score.guilds
            + Score.wonders
            + Score.tokens
            + Score.coins
            + Score.military
        ).label("total"),
    )

    if game_id:
        statement = statement.where(Score.game_id == game_id)

    scores = session.exec(statement).all()

    return scores
