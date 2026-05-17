# backend/app/api_client.py

import httpx
from typing import List, Dict, Any
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

API_BASE_URL = "https://api.randomdatatools.ru"

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def fetch_random_people(count: int) -> List[Dict[str, Any]]:
    """Загружает `count` случайных людей из внешнего API и приводит поля к нужному формату."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{API_BASE_URL}/?count={count}&params=LastName,FirstName,Gender,Phone,Email,Address"
        )
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, list):
            return []

        transformed_data = []
        for item in data:
            transformed_item = {
                "last_name": item.get("LastName"),
                "first_name": item.get("FirstName"),
                "gender": item.get("Gender"),
                "phone": item.get("Phone"),
                "email": item.get("Email"),
                "location": item.get("Address"),
            }
            transformed_data.append(transformed_item)

        return transformed_data