from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.dialects import postgresql
from sqlmodel import Session, select

from app.api.util import get_session
from app.models.game import Game
from app.models.player import Player
from app.models.score import Score

router = APIRouter()


@router.get("/wins")
def get_wins(
    session: Session = Depends(get_session),
):

    total_score_cte = select(
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
    ).cte()

    statement = (
        select(
            total_score_cte.c.game_id,
            Game.date.label("game_date"),
            Player.name.label("winner"),
        )
        .distinct(Game.id)
        .join(Game, total_score_cte.c.game_id == Game.id)
        .join(Player, total_score_cte.c.player_id == Player.id)
        .order_by(Game.id, total_score_cte.c.total.desc())
    )

    statement.compile(dialect=postgresql.dialect())

    winners = session.exec(statement).all()

    return winners
