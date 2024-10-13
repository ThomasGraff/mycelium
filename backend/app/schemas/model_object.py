from typing import Dict, Optional

from pydantic import BaseModel, Field

from .field_object import FieldObject


class ModelObject(BaseModel):
    """
    Represents a model object in a data contract.

    This class defines the structure and properties of a model,
    including its description, type, and fields.
    """

    description: Optional[str] = Field(None, description="A description of the model.")
    type: str = Field("table", description="The type of the model, default is 'table'.")
    fields: Dict[str, FieldObject] = Field(..., description="The fields (e.g. columns) of the model.")
