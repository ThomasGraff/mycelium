from typing import Union

from pydantic import BaseModel, ConfigDict, Field


class SodaCLQualityObject(BaseModel):
    """
    Represents quality attributes in Soda Checks Language.
    """

    type: str = Field(
        "SodaCL",
        const=True,
        description="The type of the schema, always 'SodaCL'.",
        example="SodaCL",
    )
    specification: str = Field(
        ...,
        description="The SodaCL specification as a string or inline YAML.",
        example="""
        checks for orders:
          - row_count > 0
          - duplicate_count(order_id) = 0
        checks for line_items:
          - row_count > 0
        """,
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "SodaCL",
                "specification": """
                checks for orders:
                  - row_count > 0
                  - duplicate_count(order_id) = 0
                checks for line_items:
                  - row_count > 0
                """,
            }
        }
    )


class MonteCarloQualityObject(BaseModel):
    """
    Represents quality attributes defined as Monte Carlo's Monitors as Code.
    """

    type: str = Field(
        "montecarlo", const=True, description="The type of the schema, always 'montecarlo'.", example="montecarlo"
    )
    specification: str = Field(
        ...,
        description="The Monte Carlo specification as a string or inline YAML.",
        example="""
        montecarlo:
          field_health:
            - table: project:dataset.table_name
              timestamp_field: created
          dimension_tracking:
            - table: project:dataset.table_name
              timestamp_field: created
              field: order_status
        """,
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "montecarlo",
                "specification": """
                montecarlo:
                  field_health:
                    - table: project:dataset.table_name
                      timestamp_field: created
                  dimension_tracking:
                    - table: project:dataset.table_name
                      timestamp_field: created
                      field: order_status
                """,
            }
        }
    )


class GreatExpectationsQualityObject(BaseModel):
    """
    Represents quality attributes defined as Great Expectations Expectations.
    """

    type: str = Field(
        "great-expectations",
        const=True,
        description="The type of the schema, always 'great-expectations'.",
        example="great-expectations",
    )
    specification: dict = Field(
        ...,
        description="The Great Expectations specification as a dictionary.",
        example={
            "orders": """
            [
                {
                    "expectation_type": "expect_table_row_count_to_be_between",
                    "kwargs": {
                        "min_value": 10
                    },
                    "meta": {}
                }
            ]
            """
        },
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "great-expectations",
                "specification": {
                    "orders": """
                    [
                        {
                            "expectation_type": "expect_table_row_count_to_be_between",
                            "kwargs": {
                                "min_value": 10
                            },
                            "meta": {}
                        }
                    ]
                    """
                },
            }
        }
    )


class CustomQualityObject(BaseModel):
    """
    Represents custom quality attributes.
    """

    type: str = Field(
        "custom",
        const=True,
        description="The type of the schema, always 'custom'.",
        example="custom",
    )
    specification: str = Field(
        ...,
        description="The custom specification as a string.",
        example="Custom quality specification goes here.",
    )

    model_config = ConfigDict(
        json_schema_extra={"example": {"type": "custom", "specification": "Custom quality specification goes here."}}
    )


class QualityObject(BaseModel):
    """
    Represents the quality object containing quality attributes and checks.

    :param str type: REQUIRED. The type of the schema (e.g., 'SodaCL', 'montecarlo', 'great-expectations', 'custom').
    :param Union[SodaCLQualityObject, MonteCarloQualityObject, GreatExpectationsQualityObject, CustomQualityObject] specification: REQUIRED. The specification of the quality attributes.
    """

    type: str = Field(..., description="REQUIRED. The type of the schema.", example="SodaCL")
    specification: Union[
        SodaCLQualityObject,
        MonteCarloQualityObject,
        GreatExpectationsQualityObject,
        CustomQualityObject,
    ] = Field(
        ...,
        description="REQUIRED. The specification of the quality attributes.",
        example=SodaCLQualityObject.model_config.json_schema_extra["example"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "SodaCL",
                "specification": SodaCLQualityObject.model_config.json_schema_extra["example"],
            }
        }
    )
