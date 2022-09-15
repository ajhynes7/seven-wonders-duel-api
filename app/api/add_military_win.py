from fastapi import Depends
from fastapi.routing import APIRouter
from sqlmodel.orm.session import Session

from app.api.util import get_session
from app.models.military_supremacy import MilitarySupremacy

router = APIRouter()


@router.post("/wins/military", status_code=201)
def add_military_win(
    military_supremacy: MilitarySupremacy, session: Session = Depends(get_session)
):
    session.add(military_supremacy)
    session.commit()
    session.refresh(military_supremacy)

    return military_supremacy
