from typing import Optional

from pydantic import BaseModel, Field


class ServerObject(BaseModel):
    """
    Represents a server object in a data contract.

    This class defines the structure and properties of a server,
    including its type, location, format, and delimiter.
    """

    type: str = Field(..., description="The type of the data product technology that implements the data contract.")
    location: str = Field(..., description="The location of the server.")
    format: Optional[str] = Field(None, description="File format.")
    delimiter: Optional[str] = Field(
        None, description="Only for format = json. How multiple json documents are delimited within one file"
    )
