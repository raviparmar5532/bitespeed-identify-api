from fastapi import FastAPI, APIRouter, Depends, HTTPException
from database import Base, engine
import schemas, services, database
from sqlalchemy.orm import Session
import asyncio

app = FastAPI()

Base.metadata.create_all(bind=engine)

identify_lock = asyncio.Lock()

@app.post("/identify", response_model=schemas.IdentifyResponse)
async def identify(payload: schemas.IdentifyRequest, db: Session = Depends(database.get_db)):
    if not payload.email and not payload.phoneNumber:
        raise HTTPException(status_code=400, detail="At least email or phoneNumber is required")
    async with identify_lock:
        return await services.identify_service(payload.email, payload.phoneNumber, db)