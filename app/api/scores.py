from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from app.api.util import get_session
from app.models.game import Game
from app.models.player import Player
from app.models.score import Score

router = APIRouter()


@router.get("/scores")
def get_scores(
    game_id: int | None = None,
    session: Session = Depends(get_session),
):
    statement = (
        select(
            Game.id.label("game_id"),
            Game.date.label("game_date"),
            Player.name.label("player_name"),
            Score.civilian,
            Score.science,
            Score.commerce,
            Score.guilds,
            Score.wonders,
            Score.tokens,
            Score.coins,
            Score.military,
        )
        .join(Game, Score.game_id == Game.id)
        .join(Player, Score.player_id == Player.id)
        .order_by(Game.id, Player.id)
    )

    if game_id:
        statement = statement.where(Score.game_id == game_id)

    scores = session.exec(statement).all()

    return scores


@router.get("/scores/total")
def get_total_scores(
    game_id: int | None = None,
    session: Session = Depends(get_session),
):
    statement = (
        select(
            Game.id.label("game_id"),
            Game.date.label("game_date"),
            Player.name.label("player_name"),
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
        .join(Game, Score.game_id == Game.id)
        .join(Player, Score.player_id == Player.id)
    )

    if game_id:
        statement = statement.where(Score.game_id == game_id)

    scores = session.exec(statement).all()

    return scores


@router.post("/scores", status_code=201)
def add_score(score: Score, session: Session = Depends(get_session)):
    session.add(score)

    try:
        session.commit()
    except Exception:
        raise HTTPException(status_code=403)

    session.refresh(score)

    return score
