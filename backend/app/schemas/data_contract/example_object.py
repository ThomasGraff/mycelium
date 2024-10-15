from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ExampleObject(BaseModel):
    """
    Represents an example object in a data contract.

    This class defines the structure and properties of an example,
    including its type, data, description, and associated model.
    """

    type: str = Field(
        ...,
        description="The type of the data product technology that implements the data contract.",
        examples=["csv", "json", "yaml", "custom"],
    )
    description: Optional[str] = Field(
        None,
        description="An optional string describing the example.",
        example="An example list of order records.",
    )
    model: str = Field(
        ...,
        description="The reference to the model in the schema, e.g. a table name.",
        example="orders",
    )
    data: str = Field(
        ...,
        description="Example data for this model.",
        example="order_id,order_timestamp,order_total\n" '"1001","2023-09-09T08:30:00Z",2500\n',
    )

    model_config = ConfigDict(
        {
            "json_schema_extra": {
                "example": {
                    "type": "csv",
                    "description": "An example list of order records.",
                    "model": "orders",
                    "data": "order_id,order_timestamp,order_total\n"
                    '"1001","2023-09-09T08:30:00Z",2500\n'
                    '"1002","2023-09-08T15:45:00Z",1800\n'
                    '"1003","2023-09-07T12:15:00Z",3200\n'
                    '"1004","2023-09-06T19:20:00Z",1500\n'
                    '"1005","2023-09-05T10:10:00Z",4200\n'
                    '"1006","2023-09-04T14:55:00Z",2800\n'
                    '"1007","2023-09-03T21:05:00Z",1900\n'
                    '"1008","2023-09-02T17:40:00Z",3600\n'
                    '"1009","2023-09-01T09:25:00Z",3100\n'
                    '"1010","2023-08-31T22:50:00Z",2700',
                }
            }
        }
    )
