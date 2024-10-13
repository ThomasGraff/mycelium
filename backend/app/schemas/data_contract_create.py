from pydantic import BaseModel, ConfigDict, Field

from .data_contracts import DataContract


class DataContractCreate(DataContract):
    """
    Represents the input model for creating a new data contract.
    Inherits all fields from the base DataContract model.
    """

    pass


class DataContractCreateResponse(BaseModel):
    """
    Represents the response for a successful data contract creation.

    :param str message: A success message indicating the data contract was created.
    :param DataContract data: The created data contract.
    """

    message: str = Field(..., description="A success message indicating the data contract was created.")
    data: DataContract = Field(..., description="The created data contract.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": " ✅ Data contract created successfully",
                "data": DataContract.model_config["json_schema_extra"]["example"],
            }
        }
    )
