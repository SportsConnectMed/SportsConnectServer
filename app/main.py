from fastapi import FastAPI

from app.modules.users.api.routes.user_routes import router as user_router
from app.modules.auth.api.routes.auth_routes import router as auth_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
async def health():
    return {"message": "Hello world"}
