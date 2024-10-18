from pydantic import ConfigDict, Field

from ..data_contract.data_contract import DataContract
from ...utils.example_model import BaseModelWithExample

class DataContractUpdate(DataContract):
    """
    Represents the input model for updating an existing data contract.
    All fields are optional to allow partial updates.
    """

    pass


class DataContractUpdateResponse(BaseModelWithExample):
    """
    Represents the response for a successful data contract update.

    :param str message: A success message indicating the data contract was updated.
    :param DataContract data: The updated data contract.
    """

    message: str = Field(
        ...,
        example=" ✅ Data contract updated successfully",
        description="A success message indicating the data contract was updated.",
    )
    data: DataContract = Field(
        ...,
        example=DataContract.example(),
        description="The updated data contract.",
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)
