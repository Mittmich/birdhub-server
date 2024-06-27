from fastapi import Depends, FastAPI
from .data.settings import Settings, get_settings
from .routes import detections, effector_action, recordings


app = FastAPI()
app.include_router(detections.router)
app.include_router(effector_action.router)
app.include_router(recordings.router)


@app.get("/")
async def root(settings: Settings = Depends(get_settings)):
    return {"message": f"Welcome to {settings.app_name}!"}
