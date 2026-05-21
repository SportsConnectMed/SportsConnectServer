from fastapi import FastAPI

from app.modules.auth.api.routes.auth_routes import router as auth_router
from app.modules.matches.api.routes.match_routes import router as match_router
from app.modules.users.api.routes.user_routes import router as user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(match_router)


@app.get("/")
async def health():
    return {"message": "Hello world"}
