from fastapi import FastAPI
from app.routes.create_problem import router 

app = FastAPI(
        title="Create Problems by AI",
        description="This system allows users to create coding problems using AI.",
        version="1.0.0",
)

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to the Create Problems by AI API!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}