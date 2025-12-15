from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Welcome to Zaytun API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", reload=True)
