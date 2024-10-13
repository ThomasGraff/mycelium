from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class InfoObject(BaseModel):
    """
    Represents the metadata information of a data contract.

    This class defines the structure for the 'info' section of a data contract,
    including details such as title, version, description, owner, and contact information.
    """

    title: str = Field(..., description="The title of the data contract.")
    version: str = Field(..., description="The version of the data contract document.")
    description: Optional[str] = Field(None, description="A description of the data contract.")
    owner: Optional[str] = Field(
        None, description="The owner or team responsible for managing the data contract and providing the data."
    )
    contact: Optional[Dict[str, Any]] = Field(None, description="Contact information for the data contract.")
