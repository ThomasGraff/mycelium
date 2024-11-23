from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .utils.config import settings
from .supabase.client import supabase_client
from .routers import auth, data_contract

logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Mycelium API",
        description="API for managing data contracts with Supabase integration",
        version="1.0.0"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize Supabase client
    try:
        supabase_client.get_client()
        logger.info("✅ Supabase client initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Supabase client: {str(e)}")
        raise

    # Include routers
    app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
    app.include_router(data_contract.router, prefix="/data-contracts", tags=["Data Contracts"])

    return app

app = create_app()
