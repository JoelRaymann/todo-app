from fastapi import FastAPI
from app.core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

# Import Models
from app.models.user_model import UserModel

# Import Router
from app.api.v1.router import api_vi_router

app = FastAPI(
    # Project Meta-data
    title=settings.PROJECT_NAME,

    # Generates the Documentations Schema
    # root_path=f'{settings.API_V1_STRING}',
)


@app.on_event('startup')
async def app_init() -> None:
    """
    Initialize crucial application services
    """

    # Connect to MongoDB and create DB="todolist"
    db_client = AsyncIOMotorClient(settings.MONGODB_CONNECTION_STRING).todolist

    # print(db_client)

    await init_beanie(
        database=db_client,
        document_models=[
            UserModel
        ]
    )


# Include Routers
app.include_router(router=api_vi_router, prefix=settings.API_V1_STRING)
