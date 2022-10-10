from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.functions import coalesce, count
from sqlmodel import Session, select

from app.api.util import get_session
from app.models.game import Game
from app.models.player import Player
from app.models.score import Score
from app.models.supremacy import Supremacy

router = APIRouter()


def get_game_winners_cte():

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

    return (
        select(
            Game.id.label("game_id"),
            coalesce(
                score_winners.c.player_id,
                Supremacy.player_id,
            ).label("player_id"),
        )
        .distinct(Game.id)
        .outerjoin(score_winners, Game.id == score_winners.c.game_id)
        .outerjoin(Supremacy, Game.id == Supremacy.game_id)
        .order_by(Game.id)
    ).cte()


@router.get("/wins")
def get_wins(
    game_id: int | None = None,
    session: Session = Depends(get_session),
):

    game_winners = get_game_winners_cte()

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


@router.get("/wins/total")
def get_total_wins(
    session: Session = Depends(get_session),
):

    game_winners = get_game_winners_cte()

    statement = (
        select(Player.name.label("player_name"), count().label("total_wins"))
        .join(game_winners, Player.id == game_winners.c.player_id)
        .group_by(Player.id)
        .order_by(Player.id)
    )

    statement.compile(dialect=postgresql.dialect())

    return session.exec(statement).all()
