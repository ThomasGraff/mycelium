from pydantic import BaseModel, ConfigDict, Field

from ..data_contract.data_contract import DataContract


class DataContractDelete(BaseModel):
    """
    Represents the input model for deleting an existing data contract.
    """

    id: str = Field(..., description="The unique identifier of the data contract to delete.")
    model_config = ConfigDict(json_schema_extra={"example": {"id": "urn:datacontract:checkout:orders-latest"}})


class DataContractDeleteResponse(BaseModel):
    """
    Represents the response for a successful data contract deletion.
    """

    message: str = Field(..., description="A success message indicating the data contract was deleted.")
    data: DataContract = Field(..., description="The deleted data contract information.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": " ✅ Data contract deleted successfully",
                "data": DataContract.model_config["json_schema_extra"]["example"],
            }
        }
    )
