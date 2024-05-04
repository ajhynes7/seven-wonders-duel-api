from sqlmodel import Session, create_engine


def get_session():
    engine = create_engine("postgresql://localhost:5432/seven_wonders_duel")

    with Session(engine) as session:
        yield session
