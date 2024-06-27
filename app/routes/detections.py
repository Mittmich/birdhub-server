from fastapi import APIRouter, Depends
from datetime import datetime
from typing import Optional
from ..data.crud import add_detections, get_detections_time_range, get_all_detections
from ..data.schemas import DetectionPost, DetectionGet
from ..data.database import get_db


router = APIRouter()


@router.get("/detections/", tags=["detections"])
async def read_detections(
    start: Optional[datetime] = None, end: Optional[datetime] = None, db=Depends(get_db)
) -> list[DetectionGet]:
    """Returns paginated detections, based on the time filters provided."""
    if start is None and end is None:
        return get_all_detections(db)
    return get_detections_time_range(db, start, end)


@router.post("/detections/", tags=["detections"])
async def post_detections(detections: DetectionPost, db=Depends(get_db)):
    """Add detections to the database."""
    add_detections(db, detections.detections)
    return {"message": "Detections added successfully!"}
