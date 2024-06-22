from fastapi import Depends, FastAPI


from .routes import detections


app = FastAPI()
app.include_router(detections.router)



@app.get("/")
async def root():
    return {"message": "Welcome to birdhub!"}