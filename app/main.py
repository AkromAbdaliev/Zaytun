from fastapi import FastAPI

from app.categories.router import router as categories_router
from app.listings.router import router as listings_router
from app.users.auth.router import router as auths_router
from app.users.router import router as users_router

app = FastAPI()

app.include_router(auths_router)
app.include_router(users_router)
app.include_router(categories_router)
app.include_router(listings_router)


@app.get("/")
async def read_root():
    return {"message": "Welcome to Zaytun API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", reload=True)
