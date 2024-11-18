from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db


# @asynccontextmanager
async def life_span(app: FastAPI):
    print("Starting server")
    await init_db()
    yield
    print("Closing server")


version = "v1"
app = FastAPI(
    title="Book API",
    description="A REST API for books review web service",
    version=version,
    # lifespan=life_span,
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
