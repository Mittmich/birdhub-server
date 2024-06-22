from fastapi import APIRouter

router = APIRouter()


@router.get("/detections/", tags=["detections"])
async def read_detections():
    """Returns paginated detections, based on the time filters provided."""
    return {"message": "This is a placeholder for the detections endpoint."}


@router.post("/detections/", tags=["detections"])
async def read_detections():
    """Add detections to the database."""
    return {"message": "This is a placeholder for the detections endpoint."}