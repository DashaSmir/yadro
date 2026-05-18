import pytest
import respx
from httpx import Response
from app.api_client import fetch_random_people

@pytest.mark.asyncio
async def test_fetch_random_people_success(respx_mock):
    """Успешная загрузка"""
    mock_data = [
        {
            "LastName": "Иванов",
            "FirstName": "Иван",
            "Gender": "Мужчина",
            "Phone": "+7 123 456-78-90",
            "Email": "ivan@example.com",
            "Address": "Москва, ул. Ленина, 1"
        }
    ]
    respx_mock.get("https://api.randomdatatools.ru/?count=1&params=LastName,FirstName,Gender,Phone,Email,Address").mock(
        return_value=Response(200, json=mock_data)
    )
    result = await fetch_random_people(1)
    assert len(result) == 1
    assert result[0]["last_name"] == "Иванов"
    assert result[0]["first_name"] == "Иван"
    assert result[0]["gender"] == "Мужчина"
    assert result[0]["phone"] == "+7 123 456-78-90"
    assert result[0]["email"] == "ivan@example.com"
    assert result[0]["location"] == "Москва, ул. Ленина, 1"

@pytest.mark.asyncio
async def test_fetch_random_people_empty(respx_mock):
    """должен вернуться пустой список от api"""
    respx_mock.get("https://api.randomdatatools.ru/?count=5&params=LastName,FirstName,Gender,Phone,Email,Address").mock(
        return_value=Response(200, json={"error": "something"})
    )
    result = await fetch_random_people(5)
    assert result == []

@pytest.mark.asyncio
async def test_fetch_random_people_http_error(respx_mock):
    """Ошибка HTTP (404, 500 и т.п.) должна вызывать исключение."""
    respx_mock.get("https://api.randomdatatools.ru/?count=10&params=LastName,FirstName,Gender,Phone,Email,Address").mock(
        return_value=Response(404)
    )
    with pytest.raises(Exception):
        await fetch_random_people(10)