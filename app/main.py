

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from psycopg_pool import AsyncConnectionPool

from app.core.config import settings
from app.api.router import api_router
from app.services.vector_store import vector_store_service 
from app.db.init_db import init_db

# 1. Initialize Vector Store 
# 2. Initialize Postgres Pool
# 3. Check for tables in postgres
# Initialize the app with the lifespan logic


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("🔌 Checking Vector Store connection...")
    vector_store_service.ensure_vectoredb_exists()

    print("🏊 Creating Database Pool...")
    app.state.pool = AsyncConnectionPool(
        conninfo=settings.DB_URI,
        max_size=20,
        kwargs={"autocommit": True},
        open=False
    )
    
    await app.state.pool.open()
    try:
        print("🛠️  Checking database schema...")
        await init_db(app.state.pool)
    except Exception as e:
        print(f"❌ Failed to initialize database tables: {e}")

    print("✅ All systems ready!")
    yield 
    
    print("🛑 Shutting down...")
    await app.state.pool.close()
    print("👋 Goodbye!")


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
def health_check():
    return {"status": "running"}