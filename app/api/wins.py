from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.functions import coalesce
from sqlmodel import Session, select

from app.api.util import get_session
from app.models.game import Game
from app.models.military_supremacy import MilitarySupremacy
from app.models.player import Player
from app.models.scientific_supremacy import ScientificSupremacy
from app.models.score import Score

router = APIRouter()


@router.get("/wins")
def get_wins(
    game_id: int | None = None,
    session: Session = Depends(get_session),
):

    total_scores = select(
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

    score_winners = (
        select(total_scores.c.game_id, total_scores.c.player_id)
        .distinct(total_scores.c.game_id)
        .order_by(total_scores.c.game_id, total_scores.c.total.desc())
    ).cte()

    game_winners = (
        select(
            Game.id.label("game_id"),
            coalesce(
                score_winners.c.player_id,
                MilitarySupremacy.player_id,
                ScientificSupremacy.player_id,
            ).label("player_id"),
        )
        .distinct(Game.id)
        .outerjoin(score_winners, Game.id == score_winners.c.game_id)
        .outerjoin(MilitarySupremacy, Game.id == MilitarySupremacy.game_id)
        .outerjoin(ScientificSupremacy, Game.id == ScientificSupremacy.game_id)
        .order_by(Game.id)
    ).cte()

    statement = (
        select(
            game_winners.c.game_id,
            Game.date.label("game_date"),
            Player.name.label("winner"),
        )
        .join(Player, game_winners.c.player_id == Player.id)
        .join(Game, game_winners.c.game_id == Game.id)
        .order_by(Game.id)
    )

    if game_id:
        statement = statement.where(Game.id == game_id)

    statement.compile(dialect=postgresql.dialect())

    return session.exec(statement).all()
