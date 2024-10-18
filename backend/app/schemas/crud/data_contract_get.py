from pydantic import BaseModel, ConfigDict, Field

from ..data_contract.data_contract import DataContract
from ...utils.example_model import BaseModelWithExample

class DataContractGetResponse(BaseModelWithExample):
    """
    Represents the response for a successful data contract retrieval.
    """

    message: str = Field(
        ...,
        example=" ✅ Data contract retrieved successfully",
        description="A success message indicating the data contract was retrieved.",
    )
    data: DataContract = Field(
        ...,
        example=DataContract.example(),
        description="The retrieved data contract.",
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)
