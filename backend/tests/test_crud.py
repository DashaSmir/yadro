import pytest
from app import crud, schemas

@pytest.mark.asyncio
async def test_create_and_get_person(db_session):
    person_data = schemas.PersonCreate(
        gender="Женщина",
        first_name="Анна",
        last_name="Петрова",
        phone="+7 999 111-22-33",
        email="anna@example.com",
        location="Санкт-Петербург"
    )
    created = await crud.create_person(db_session, person_data)
    assert created.id is not None

    fetched = await crud.get_person(db_session, created.id)
    assert fetched.email == "anna@example.com"

@pytest.mark.asyncio
async def test_bulk_insert_ignores_duplicates(db_session):
    data = [
        {"gender": "M", "first_name": "A", "last_name": "B", "phone": "1", "email": "dup@example.com", "location": "Loc"},
        {"gender": "F", "first_name": "C", "last_name": "D", "phone": "2", "email": "dup@example.com", "location": "Loc2"}, 
        {"gender": "M", "first_name": "E", "last_name": "F", "phone": "3", "email": "unique@example.com", "location": "Loc3"}
    ]
    inserted = await crud.create_people_bulk(db_session, data)
    assert len(inserted) == 2 
    assert inserted[0].email == "dup@example.com"
    assert inserted[1].email == "unique@example.com"

@pytest.mark.asyncio
async def test_pagination(db_session):
    # Вставляем 25 записей
    for i in range(25):
        await crud.create_person(db_session, schemas.PersonCreate(
            gender="M", first_name=f"Name{i}", last_name="Test", phone="123", email=f"user{i}@test.com", location="City"
        ))
    page = await crud.get_people_paginated(db_session, skip=0, limit=20)
    assert len(page) == 20
    total = await crud.get_total_count(db_session)
    assert total == 25

@pytest.mark.asyncio
async def test_random_person(db_session):
    # Сначала нет записей
    random = await crud.get_random_person(db_session)
    assert random is None
    # Добавляем одну
    await crud.create_person(db_session, schemas.PersonCreate(
        gender="F", first_name="Random", last_name="Test", phone="000", email="random@test.com", location="Any"
    ))
    random = await crud.get_random_person(db_session)
    assert random is not None
    assert random.email == "random@test.com"