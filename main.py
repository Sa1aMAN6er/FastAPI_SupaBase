from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from databases import Database
from config import DATABASE_URL  # Импортируем строку подключения
from fastapi import FastAPI

#Подключение к базе с помощью SQLAlchemy и Databases
database = Database(DATABASE_URL)
engine = create_async_engine(DATABASE_URL, future=True, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

#Команда для запуска базы в FastAPI
app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    
#Чтобы убедиться, что FastAPI подключился к Supabase, добавь тестовый эндпоинт
@app.get("/ping_db")
async def ping_db():
    try:
        conn = await database.connect()
        await database.disconnect()
        return {"message": "Connected to Supabase!"}
    except Exception as e:
        return {"error": str(e)}
