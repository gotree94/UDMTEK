"""
Database configuration and connection management
"""
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

logger = logging.getLogger(__name__)

# Database URL (will be loaded from environment)
DATABASE_URL = "postgresql+asyncpg://udmtek_user:udmtek_password_2024@localhost:5432/udmtek"

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=False,
)

# Create async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for models
Base = declarative_base()


async def init_db():
    """Initialize database connection and create tables"""
    logger.info("Initializing database connection...")
    
    try:
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("✅ Database initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        raise


async def close_db():
    """Close database connection"""
    logger.info("Closing database connection...")
    
    try:
        await engine.dispose()
        logger.info("✅ Database connection closed")
        
    except Exception as e:
        logger.error(f"❌ Failed to close database: {str(e)}")


async def get_db():
    """Dependency for getting database session"""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
