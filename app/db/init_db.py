from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

async def init_db(pool: AsyncConnectionPool):
    """
    Checks for required tables and creates them if they don't exist.
    """
    
    print("🧠 Setting up LangGraph checkpoint tables...")
    try:
        checkpointer = AsyncPostgresSaver(pool)
        await checkpointer.setup()
        print("LangGraph tables created.")
    except Exception as e:
        print(f"Warning: LangGraph table setup failed: {e}")

    async with pool.connection() as conn:
        async with conn.cursor() as cur:

            await cur.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')

            await cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    email TEXT UNIQUE NOT NULL,
                    username TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)

            await cur.execute("""
                CREATE TABLE IF NOT EXISTS user_files (
                    id SERIAL PRIMARY KEY,
                    user_id UUID NOT NULL REFERENCES users(id),
                    filename VARCHAR(255) NOT NULL,
                    file_path TEXT NOT NULL,
                    file_size BIGINT,
                    status VARCHAR(50) DEFAULT 'queued',
                    stage VARCHAR(50) DEFAULT 'init',
                    job_stats JSONB DEFAULT '{}'::jsonb,
                    chunk_count INT DEFAULT 0,
                    vector_count INT DEFAULT 0,
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)


            await cur.execute("""
                CREATE TABLE IF NOT EXISTS threads (
                    thread_id UUID PRIMARY KEY,
                    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                    title TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            print("Tables checked/created successfully.")