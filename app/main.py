from fastapi import Depends, FastAPI
from .data.settings import Settings, get_settings
from .routes import detections


app = FastAPI()
app.include_router(detections.router)


@app.get("/")
async def root(settings: Settings = Depends(get_settings)):
    return {"message": f"Welcome to {settings.app_name}!"}