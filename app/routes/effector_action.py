from fastapi import APIRouter, Depends
from ..data.crud import add_effector_action
from ..data.schemas import EffectorActionPost
from ..data.database import get_db


router = APIRouter()


@router.post("/effectorAction/", tags=["effectorAction"])
async def post_effector_action(effect_activation: EffectorActionPost, db=Depends(get_db)):
    """Add effector action to the database."""
    add_effector_action(db, effect_activation)
    return {"message": "Effect activation added successfully!"}