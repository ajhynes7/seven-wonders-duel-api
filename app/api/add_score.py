from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlmodel import Session

from app.api.util import get_session
from app.models.score import Score

router = APIRouter()


@router.post("/scores", status_code=201)
def add_score(score: Score, session: Session = Depends(get_session)):

    session.add(score)

    try:
        session.commit()
    except Exception:
        raise HTTPException(status_code=403)

    session.refresh(score)

    return score
