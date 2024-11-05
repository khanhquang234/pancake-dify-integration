# src/main.py
from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Pancake-Dify Integration")

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)