from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.db import Base, engine
from app.routers import auth, credentials, resources

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Multi-Cloud Free-Tier Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(credentials.router)
app.include_router(resources.router)


@app.get("/health")
def health():
    return {"status": "ok"}
