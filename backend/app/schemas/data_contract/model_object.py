from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, Field

from .config_object import ConfigObject
from .field_object import FieldObject


class ModelObject(BaseModel):
    """
    Represents a model object in a data contract.

    This class defines the structure and properties of a data model,
    such as tables, views, or structured files.
    """

    type: str = Field(
        default="table",
        description="The type of the model. Examples: table, view, object.",
        example="table",
    )
    description: Optional[str] = Field(
        None,
        description="An optional string describing the data model.",
        example="One record per order. Includes cancelled and deleted orders.",
    )
    title: Optional[str] = Field(
        None,
        description="An optional string for the title of the data model. "
        "Especially useful if the name of the model is cryptic or contains abbreviations.",
        example="Orders Latest",
    )
    fields: Dict[str, FieldObject] = Field(
        ...,
        description="The fields (e.g. columns) of the data model.",
        example={
            "order_id": FieldObject(
                description="Unique identifier for the order",
                type="string",
                format="uuid",
                required=True,
                unique=True,
                primary=True,
                example="243c25e5-a081-43a9-aeab-6d5d5b6cb5e2",
            ),
            "order_timestamp": FieldObject(
                description="Timestamp of the order",
                type="timestamp",
                required=True,
                example="2024-09-09T08:30:00Z",
            ),
        },
    )
    config: Optional[ConfigObject] = Field(
        None,
        description="Any additional key-value pairs that might be useful for further tooling.",
        example={"partition_key": "order_timestamp", "clustering_key": "order_id"},
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "table",
                "description": "One record per order. Includes cancelled and deleted orders.",
                "title": "Orders Latest",
                "fields": {
                    "order_id": {
                        "description": "An internal ID that identifies an order in the online shop.",
                        "type": "text",
                        "format": "uuid",
                        "required": True,
                        "unique": True,
                        "primary": True,
                        "example": "243c25e5-a081-43a9-aeab-6d5d5b6cb5e2",
                        "pii": True,
                        "classification": "restricted",
                        "tags": ["orders"],
                    },
                    "order_timestamp": {
                        "description": "The business timestamp in UTC when the order was successfully registered in the source system and the payment was successful.",
                        "type": "timestamp",
                        "required": True,
                        "example": "2024-09-09T08:30:00Z",
                    },
                    "order_total": {
                        "description": "Total amount in the smallest monetary unit (e.g., cents).",
                        "type": "long",
                        "required": True,
                        "example": 9999,
                    },
                    "customer_id": {
                        "description": "Unique identifier for the customer.",
                        "type": "text",
                        "minLength": 10,
                        "maxLength": 20,
                        "example": "1000000001",
                    },
                    "customer_email_address": {
                        "description": "The email address, as entered by the customer. The email address was not verified.",
                        "type": "text",
                        "format": "email",
                        "required": True,
                        "pii": True,
                        "classification": "sensitive",
                        "example": "mary.taylor82@example.com",
                    },
                    "processed_timestamp": {
                        "description": "The timestamp when the record was processed by the data platform.",
                        "type": "timestamp",
                        "required": True,
                        "example": "2030-09-09T08:31:00Z",
                        "config": {
                            "jsonType": "string",
                            "jsonFormat": "date-time",
                        },
                    },
                },
                "config": ConfigObject.model_config["json_schema_extra"]["example"],
            }
        }
    )
