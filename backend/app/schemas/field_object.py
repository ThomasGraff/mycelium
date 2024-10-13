from typing import Optional

from pydantic import BaseModel, Field


class FieldObject(BaseModel):
    """
    Represents a field object in a data contract model.

    This class defines the structure and properties of a field,
    including its description, type, requirements, uniqueness, and sensitivity.
    """

    description: Optional[str] = Field(None, description="A description of the field.")
    type: str = Field(..., description="The data type of the field.")
    required: Optional[bool] = Field(None, description="Indicates if the field is required.")
    unique: Optional[bool] = Field(None, description="Indicates if the field values must be unique.")
    primary: Optional[bool] = Field(None, description="Indicates if the field is a primary key.")
    pii: Optional[bool] = Field(
        None, description="Indicates if the field contains Personal Identifiable Information (PII)."
    )
    classification: Optional[str] = Field(
        None, description="The data class defining the sensitivity level for this field."
    )
