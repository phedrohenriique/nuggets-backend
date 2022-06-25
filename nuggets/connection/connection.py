import configuration as config
import asyncpg

## creates a pool connection with the database parameters ready to be used

async def create_pool():
    connection = 'postgres://{user}:{password}@{host}:{port}/{database}'.format(
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT,
        database=config.DB_NAME
    )

    pool = await asyncpg.create_pool(
        dsn=connection,
        statement_cache_size=0
        )
    return pool