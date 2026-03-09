from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Footprint
from schemas import FootprintCreate

router = APIRouter()


@router.post("/save-footprint")
def save_footprint(data: FootprintCreate, db: Session = Depends(get_db)):

    footprint = Footprint(**data)

    db.add(footprint)
    db.commit()
    db.refresh(footprint)

    return footprint


@router.get("/user/{user_id}/footprints")
def get_history(user_id: int, db: Session = Depends(get_db)):

    results = db.query(Footprint).filter(
        Footprint.user_id == user_id
    ).all()

    return results