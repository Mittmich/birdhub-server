from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from typing import Optional
from ..data.crud import add_detections, get_detections_time_range, get_all_detections, aggregate_detections_per_interval
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


@router.get("/detections/stats/", tags=["detections"])
async def get_detection_stats(db=Depends(get_db)):
    """Get the number of detections in a given time range."""
    # Get the number of detections today
    start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end = datetime.now()
    detections = get_detections_time_range(db, start, end)
    # Get the number of detections in the last 7 days
    start = datetime.now() - timedelta(days=7)
    detections_7_days = get_detections_time_range(db, start, end)
    # Get the number of detections in the last 30 days
    start = datetime.now() - timedelta(days=30)
    detections_30_days = get_detections_time_range(db, start, end)
    return {
        "today": len(detections),
        "7_days": len(detections_7_days),
        "30_days": len(detections_30_days),
    }

@router.get("/detections/aggregates/", tags=["detections"])
async def get_detections_per_interval(
    start: datetime, end: datetime, interval: str, db=Depends(get_db)
):
    """Get the number of detections per interval in a given time range."""
    results = aggregate_detections_per_interval(db, start, end, interval)
    return [{"timestamp": result[0], "count": result[1]} for result in results]
    