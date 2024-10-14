from typing import List

from pydantic import BaseModel, ConfigDict, Field

from .data_contracts import DataContract


class DataContractListResponse(BaseModel):
    """
    Represents the response for a successful data contract list retrieval.
    """

    message: str = Field(..., description="A success message indicating the data contracts were retrieved.")
    data: List[DataContract] = Field(..., description="The list of retrieved data contracts.")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "message": " ✅ Data contracts retrieved successfully",
                "data": DataContract.model_config["json_schema_extra"]["example"],
            }
        },
    )
