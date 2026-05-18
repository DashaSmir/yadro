from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.models import Person
from app.schemas import PersonCreate
from typing import List, Optional

async def get_person(db: AsyncSession, person_id: int) -> Optional[Person]:
    result = await db.execute(select(Person).where(Person.id == person_id))
    return result.scalar_one_or_none()

async def get_random_person(db: AsyncSession) -> Optional[Person]:
    count_result = await db.execute(select(func.count(Person.id)))
    total = count_result.scalar()
    if total == 0:
        return None
    # random_offset = await db.execute(select(func.random()) * total)
    result = await db.execute(select(Person).order_by(func.random()).limit(1))
    return result.scalar_one_or_none()

async def get_people_paginated(db: AsyncSession, skip: int = 0, limit: int = 20) -> List[Person]:
    result = await db.execute(select(Person).offset(skip).limit(limit))
    return result.scalars().all()

async def get_total_count(db: AsyncSession) -> int:
    result = await db.execute(select(func.count(Person.id)))
    return result.scalar()

async def create_person(db: AsyncSession, person: PersonCreate) -> Person:
    db_person = Person(**person.model_dump())
    db.add(db_person)
    await db.commit()
    await db.refresh(db_person)
    return db_person

# async def create_people_bulk(db: AsyncSession, people_data: List[dict]) -> List[Person]:
#     """Массовая вставка с игнорированием дубликатов по email."""
#     existing_emails = set()
#     for person_dict in people_data:
#         existing_emails.add(person_dict.get("email"))

#     result = await db.execute(select(Person.email).where(Person.email.in_(existing_emails)))
#     existing = set(result.scalars().all())
#     new_people = [Person(**p) for p in people_data if p["email"] not in existing]
#     if new_people:
#         db.add_all(new_people)
#         await db.commit()
#         for person in new_people:
#             await db.refresh(person)
#     return new_people
async def create_people_bulk(db: AsyncSession, people_data: List[dict]) -> List[Person]:
    """Массовая вставка с игнорированием дубликатов по email (включая дубликаты внутри списка)."""
    # 1. Убираем дубликаты по email внутри переданного списка (сохраняем первое вхождение)
    seen = {}
    unique_people = []
    for p in people_data:
        email = p.get("email")
        if email and email not in seen:
            seen[email] = True
            unique_people.append(p)
    if not unique_people:
        return []

    # 2. Запрашиваем email, которые уже есть в БД
    emails = [p["email"] for p in unique_people]
    result = await db.execute(select(Person.email).where(Person.email.in_(emails)))
    existing_emails = set(result.scalars().all())

    # 3. Оставляем только тех, кого нет в БД
    new_people_data = [p for p in unique_people if p["email"] not in existing_emails]
    if not new_people_data:
        return []

    # 4. Создаём объекты и вставляем
    new_people = [Person(**p) for p in new_people_data]
    db.add_all(new_people)
    await db.commit()
    for person in new_people:
        await db.refresh(person)
    return new_people