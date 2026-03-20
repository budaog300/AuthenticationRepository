from fastapi import FastAPI
from src.auth.router import router as router_auth
from src.users.router import router as router_user
from src.modules.router import router as router_post


app = FastAPI()


@app.get("/health", summary="Проверка сервера")
async def health():
    return {"message": "success"}


app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_post)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)