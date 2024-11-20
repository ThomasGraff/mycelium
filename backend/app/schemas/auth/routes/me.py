from typing import Any, Dict

from pydantic import BaseModel


class MeResponse(BaseModel):
    """Current user info response model"""

    user: Dict[str, Any]
