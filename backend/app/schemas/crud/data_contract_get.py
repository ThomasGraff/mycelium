from pydantic import BaseModel, ConfigDict, Field

from ..data_contract.data_contract import DataContract


class DataContractGetResponse(BaseModel):
    """
    Represents the response for a successful data contract retrieval.
    """

    message: str = Field(..., description="A success message indicating the data contract was retrieved.")
    data: DataContract = Field(..., description="The retrieved data contract.")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "message": " ✅ Data contract retrieved successfully",
                "data": DataContract.model_config["json_schema_extra"]["example"],
            }
        },
    )