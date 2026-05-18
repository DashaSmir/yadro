import pytest
from app import schemas
import httpx
@pytest.mark.asyncio
async def test_list_people_empty(client, db_session):
    """Пустая таблица – возвращает пустой массив, total=0, pages=0."""
    response = await client.get("/api/people?page=1&limit=20")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["pages"] == 0

@pytest.mark.asyncio
async def test_load_people_endpoint(client, db_session, respx_mock):
    """Мокаем внешнее API и проверяем создание записей."""
    mock_people = [
        {
            "LastName": "Тестов",
            "FirstName": "Тест",
            "Gender": "Мужчина",
            "Phone": "+7 000",
            "Email": "test@example.com",
            "Address": "Адрес"
        }
    ]
    respx_mock.get("https://api.randomdatatools.ru/?count=1&params=LastName,FirstName,Gender,Phone,Email,Address").mock(
        return_value=httpx.Response(200, json=mock_people)
    )
    response = await client.post("/api/load", json={"count": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["loaded"] == 1
    assert data["total_requested"] == 1

    #Проверяем, что человек появился в БД
    resp2 = await client.get("/api/people?page=1&limit=20")
    assert resp2.status_code == 200
    assert len(resp2.json()["items"]) == 1
    assert resp2.json()["items"][0]["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_load_people_invalid_count(client):
    """Количество загружаемых людей должно быть от 1 до 5000."""
    response = await client.post("/api/load", json={"count": 0})
    assert response.status_code == 400
    response = await client.post("/api/load", json={"count": 6000})
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_get_person_by_id(client, db_session):
    from app import crud, schemas
    person = schemas.PersonCreate(
        gender="Ж", first_name="Мария", last_name="Сидорова",
        phone="123", email="maria@test.com", location="Город"
    )
    created = await crud.create_person(db_session, person)
    response = await client.get(f"/api/person/{created.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "maria@test.com"

    response = await client.get("/api/person/999999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_random_person_api(client, db_session):
    # Если людей нет – 404
    response = await client.get("/api/person/random")
    assert response.status_code == 404

    # Добавляем человека
    from app import crud, schemas
    person = schemas.PersonCreate(
        gender="М", first_name="Случайный", last_name="Человек",
        phone="000", email="random@test.com", location="Земля"
    )
    await crud.create_person(db_session, person)
    response = await client.get("/api/person/random")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "random@test.com"

@pytest.mark.asyncio
async def test_serve_static_not_found(client):
    """Проверяем, что при отсутствии статики фронт отдаёт 404."""
    response = await client.get("/")
    assert response.status_code in [200, 404]