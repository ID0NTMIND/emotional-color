from fastapi import FastAPI

app = FastAPI(title="ML Service API")


@app.get("/")
async def root():
    return {"message": "Hello from ML Service API!"}


@app.get("/health")
async def health():
    return {"status": "ok"}
