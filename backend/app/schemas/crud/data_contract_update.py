from pydantic import BaseModel, ConfigDict, Field

from ..data_contract.data_contract import DataContract


class DataContractUpdate(DataContract):
    """
    Represents the input model for updating an existing data contract.
    All fields are optional to allow partial updates.
    """

    pass


class DataContractUpdateResponse(BaseModel):
    """
    Represents the response for a successful data contract update.

    :param str message: A success message indicating the data contract was updated.
    :param DataContract data: The updated data contract.
    """

    message: str = Field(..., description="A success message indicating the data contract was updated.")
    data: DataContract = Field(..., description="The updated data contract.")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "message": " ✅ Data contract updated successfully",
                "data": DataContract.model_config["json_schema_extra"]["example"],
            }
        },
    )
