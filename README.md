# Yadro-Импульс
Приложение для загрузки и просмотра случайных людей из внешнего API. Имеет несколько частей: Backend - Python, хранение данных – PostgreSQL, 
frontend – React с кастомными стилями.

## Содержание
- [Технологии](#технологии)
- [Использование](#использование)
- [Тестирование](#тестирование)
- [Внешний вид приложения](#внешний-вид-приложения)

## Технологии
- Backend: FastAPI, SQLAlchemy async, PostgreSQL
- Frontend: React, Vite, Axios, CSS Modules
- Docker и Docker Compose
- Тесты: pytest, respx, aiosqlite


## Использование
Запуск через Docker Compose
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/DashaSmir/yadro.git
   cd yadro
   
2. Зайдите в папку проекта, запустите приложение Docker и запустите контейнеры в корневой папке:
docker-compose up --build

3. Откройте в браузере: http://localhost:8000

