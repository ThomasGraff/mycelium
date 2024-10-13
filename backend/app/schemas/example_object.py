from typing import Optional

from pydantic import BaseModel, Field


class ExampleObject(BaseModel):
    """
    Represents an example object in a data contract.

    This class defines the structure and properties of an example,
    including its type, data, description, and associated model.
    """

    type: str = Field(..., description="The type of the example data.")
    data: str = Field(..., description="The example data.")
    description: Optional[str] = Field(None, description="A description of the example data.")
    model: Optional[str] = Field(None, description="The model associated with the example data.")
