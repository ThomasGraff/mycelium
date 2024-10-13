import importlib
import logging
import os
from contextlib import asynccontextmanager
from typing import List

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info(" 💡 Data Contract Management API is starting up...")
    yield
    # Shutdown logic
    logger.info(" 💡 Data Contract Management API is shutting down...")


app = FastAPI(
    title="Data Contract Management API",
    description="An API for managing data contracts and related operations.",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


def import_routers() -> List[APIRouter]:
    """
    Dynamically imports and returns a list of routers from the 'routers' directory.

    :return List[APIRouter]: A list of imported routers.
    """
    routers = []
    routers_dir = os.path.join(os.path.dirname(__file__), "routers")
    for filename in os.listdir(routers_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f".routers.{filename[:-3]}"
            module = importlib.import_module(module_name, package=__package__)
            if hasattr(module, "router"):
                routers.append((module.router, filename[:-3]))
    return routers


# Include routers
for router, name in import_routers():
    tag = name.replace("_", " ").title()
    app.include_router(router, prefix=f"/{name}", tags=[tag])
