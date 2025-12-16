from fastapi import FastAPI

from app.users.router import router as users_router

app = FastAPI()

app.include_router(users_router)


@app.get("/")
async def read_root():
    return {"message": "Welcome to Zaytun API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", reload=True)
