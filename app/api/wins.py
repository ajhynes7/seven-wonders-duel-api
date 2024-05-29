from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy import case
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import aliased
from sqlalchemy.sql.functions import coalesce, count
from sqlmodel import Session, select

from app.api.util import get_session
from app.models.game import Game
from app.models.player import Player
from app.models.score import Score
from app.models.supremacy import Supremacy

router = APIRouter()


def get_game_winner_cte():
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

    total_score_1_cte = (
        select(
            total_score_cte.c.game_id,
            total_score_cte.c.player_id,
            total_score_cte.c.total,
        )
        .where(total_score_cte.c.player_id == 1)
        .cte()
    )
    total_score_2_cte = (
        select(
            total_score_cte.c.game_id,
            total_score_cte.c.player_id,
            total_score_cte.c.total,
        )
        .where(total_score_cte.c.player_id == 2)
        .cte()
    )

    score_winner_cte = (
        select(
            total_score_1_cte.c.game_id,
            case(
                [
                    (total_score_1_cte.c.total > total_score_2_cte.c.total, 1),
                    (total_score_1_cte.c.total < total_score_2_cte.c.total, 2),
                ],
                else_=0,
            ).label("player_id"),
        )
        .select_from(
            total_score_1_cte.join(
                total_score_2_cte,
                total_score_1_cte.c.game_id == total_score_2_cte.c.game_id,
            )
        )
        .cte()
    )

    return (
        select(
            Game.id.label("game_id"),
            coalesce(score_winner_cte.c.player_id, Supremacy.player_id).label(
                "player_id"
            ),
        )
        .select_from(Game)
        .outerjoin(score_winner_cte, Game.id == score_winner_cte.c.game_id)
        .outerjoin(Supremacy, Game.id == Supremacy.game_id)
    )


@router.get("/wins")
def get_wins(
    game_id: int | None = None,
    session: Session = Depends(get_session),
):
    game_winner_cte = get_game_winner_cte()

    statement = select(game_winner_cte.c.game_id, game_winner_cte.c.player_id).order_by(
        game_winner_cte.c.game_id
    )

    if game_id:
        statement = statement.where(game_winner_cte.c.game_id == game_id)

    return session.exec(statement).all()


@router.get("/wins/total")
def get_total_wins(
    session: Session = Depends(get_session),
):
    game_winner_cte = get_game_winner_cte()

    statement = (
        select(
            game_winner_cte.c.player_id,
            count(),
        )
        .group_by(game_winner_cte.c.player_id)
        .order_by(game_winner_cte.c.player_id)
    )

    return session.exec(statement).all()
