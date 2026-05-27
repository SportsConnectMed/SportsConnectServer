from fastapi import FastAPI

from app.modules.auth.api.routes.auth_routes import router as auth_router
from app.modules.matches.api.routes.match_routes import router as match_router
from app.modules.users.api.routes.user_routes import router as user_router

app = FastAPI()

API_PREFIX = "/api/v1"

app.include_router(user_router, prefix=API_PREFIX)
app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(match_router, prefix=API_PREFIX)


@app.get("/")
async def health():
    return {"message": "Hello world"}
