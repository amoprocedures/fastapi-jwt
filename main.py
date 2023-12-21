from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from config.settings import Config
from api.auth_route import auth_router
import uvicorn

app = FastAPI()
app.include_router(auth_router)

register_tortoise(
    app,
    db_url=Config.DB_URL,
    add_exception_handlers=True,
    generate_schemas=False,
    modules={'models': Config.DB_MODELS}
)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
