from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class ConfigObject(BaseModel):
    """
    Represents additional metadata for models and fields in a data contract.

    This class defines the structure for the 'config' section, which can be used
    to specify various properties that may be utilized by tools for tasks such as
    code generation, physical data type specification, and test toggling.
    """

    avroNamespace: Optional[str] = Field(
        None,
        description="(Only on model level) The namespace to use when importing and exporting the data model from / to Apache Avro.",
        example="my.namespace",
    )
    avroType: Optional[str] = Field(
        None,
        description="(Only on field level) Specify the field type to use when exporting the data model to Apache Avro.",
        example="long",
    )
    avroLogicalType: Optional[str] = Field(
        None,
        description="(Only on field level) Specify the logical field type to use when exporting the data model to Apache Avro.",
        example="timestamp-millis",
    )
    bigqueryType: Optional[str] = Field(
        None,
        description="(Only on field level) Specify the physical column type that is used in a BigQuery table.",
        example="NUMERIC(5, 2)",
    )
    snowflakeType: Optional[str] = Field(
        None,
        description="(Only on field level) Specify the physical column type that is used in a Snowflake table.",
        example="TIMESTAMP_LTZ",
    )
    redshiftType: Optional[str] = Field(
        None,
        description="(Only on field level) Specify the physical column type that is used in a Redshift table.",
        example="SMALLINT",
    )
    sqlserverType: Optional[str] = Field(
        None,
        description="(Only on field level) Specify the physical column type that is used in a SQL Server table.",
        example="DATETIME2",
    )
    databricksType: Optional[str] = Field(
        None,
        description="(Only on field level) Specify the physical column type that is used in a Databricks table.",
        example="TIMESTAMP",
    )
    glueType: Optional[str] = Field(
        None,
        description="(Only on field level) Specify the physical column type that is used in an AWS Glue Data Catalog table.",
        example="timestamp",
    )

    model_config = ConfigDict(
        extra="allow",  # Allows for Specification Extensions
        json_schema_extra={
            "example": {
                "avroNamespace": "my.namespace",
                "avroType": "long",
                "avroLogicalType": "timestamp-millis",
                "snowflakeType": "TIMESTAMP_TZ",
            }
        },
    )

    def __init__(self, **data: Any):
        """
        Initialize the ConfigObject with any additional fields as Specification Extensions.

        :param Dict[str, Any] data: Key-value pairs for configuration, including standard fields and extensions.
        """
        super().__init__(**data)
        for key, value in data.items():
            if not hasattr(self, key):
                setattr(self, key, value)
