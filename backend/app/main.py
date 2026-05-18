from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from app.database import engine, Base, get_db
from app import crud, schemas, api_client
import logging
import os
from pydantic import BaseModel

class LoadRequest(BaseModel):
    count: int


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(engine) as db:
        count = await crud.get_total_count(db)
        if count == 0:
            logger.info("Загрузка 1000 человек из API...")
            try:
                people_data = await api_client.fetch_random_people(1000)
                await crud.create_people_bulk(db, people_data)
            except Exception as e:
                logger.error(f"Ошибка: {e}")
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/api/people")
async def list_people(page: int = 1, limit: int = 20, db: AsyncSession = Depends(get_db)):
    skip = (page - 1) * limit
    people = await crud.get_people_paginated(db, skip=skip, limit=limit)
    total = await crud.get_total_count(db)
    return {
        "items": [schemas.PersonResponse.model_validate(p).model_dump() for p in people],
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit
    }
@app.post("/api/load")
async def load_people(request: LoadRequest, db: AsyncSession = Depends(get_db)):
    count = request.count
# @app.post("/api/load")
# async def load_people(count: int, db: AsyncSession = Depends(get_db)):
    if count <= 0 or count > 5000:
        raise HTTPException(400, "count must be 1-5000")
    people_data = await api_client.fetch_random_people(count)
    created = await crud.create_people_bulk(db, people_data)
    return {"loaded": len(created), "total_requested": count}
    
@app.get("/api/person/random", response_model=schemas.PersonResponse)
async def get_random_person_json(db: AsyncSession = Depends(get_db)):
    person = await crud.get_random_person(db)
    if not person:
        raise HTTPException(404, "No people in database")
    return person

@app.get("/api/person/{person_id}", response_model=schemas.PersonResponse)
async def get_person_json(person_id: int, db: AsyncSession = Depends(get_db)):
    person = await crud.get_person(db, person_id)
    if not person:
        raise HTTPException(404, "Person not found")
    return person

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")
    
    @app.get("/", include_in_schema=False)
    async def serve_spa():
        return FileResponse(os.path.join(static_dir, "index.html"))
    @app.get("/{full_path:path}", include_in_schema=False)
    async def catch_all(full_path: str):
        if full_path.startswith("api/"):
            # уже обработано выше
            raise HTTPException(404)
        index_path = os.path.join(static_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        raise HTTPException(404)








