from fastapi import APIRouter, Depends
from ..data.crud import add_detections
from ..data.schemas import DetectionPost
from ..data.database import get_db

router = APIRouter()


@router.get("/detections/", tags=["detections"])
async def read_detections():
    """Returns paginated detections, based on the time filters provided."""
    return {"message": "This is a placeholder for the detections endpoint."}


@router.post("/detections/", tags=["detections"])
async def post_detections(detections: DetectionPost, db=Depends(get_db)):
    """Add detections to the database."""
    add_detections(db, detections.detections)
    return {"message": "Detections added successfully!"}