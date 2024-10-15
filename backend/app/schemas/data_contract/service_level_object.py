from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AvailabilityObject(BaseModel):
    """
    Represents the availability service level for a data contract.

    This class defines the structure for the 'availability' section of service levels,
    including a description and the guaranteed uptime percentage.
    """

    description: Optional[str] = Field(
        None,
        description="A description of the availability service level.",
        example="The server is available during support hours",
    )
    percentage: Optional[str] = Field(
        None,
        description="The guaranteed uptime in percent (e.g., '99.9%').",
        example="99.9%",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "description": "The server is available during support hours",
                "percentage": "99.9%",
            }
        }
    )


class RetentionObject(BaseModel):
    """
    Represents the retention service level for a data contract.

    This class defines the structure for the 'retention' section of service levels,
    including details about how long data will be available.
    """

    description: Optional[str] = Field(
        None,
        description="A description of the retention service level.",
        example="Data is retained for one year",
    )
    period: Optional[str] = Field(
        None,
        description="The period of time data is available (e.g., '1 year', 'P1Y').",
        example="P1Y",
    )
    unlimited: Optional[bool] = Field(
        None,
        description="Indicator that data is kept forever.",
        example=False,
    )
    timestamp_field: Optional[str] = Field(
        None,
        description="Reference to the field containing the relevant timestamp.",
        example="orders.order_timestamp",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "description": "Data is retained for one year",
                "period": "P1Y",
                "unlimited": False,
                "timestamp_field": "orders.order_timestamp",
            }
        }
    )


class LatencyObject(BaseModel):
    """
    Represents the latency service level for a data contract.

    This class defines the structure for the 'latency' section of service levels,
    including details about the maximum time from source to destination.
    """

    description: Optional[str] = Field(
        None,
        description="A description of the latency service level.",
        example="Data is available within 25 hours after the order was placed",
    )
    threshold: Optional[str] = Field(
        None,
        description="Maximum duration between source and processed timestamps.",
        example="25h",
    )
    source_timestamp_field: Optional[str] = Field(
        None,
        description="Reference to the field with the source timestamp.",
        example="orders.order_timestamp",
    )
    processed_timestamp_field: Optional[str] = Field(
        None,
        description="Reference to the field with the processing timestamp.",
        example="orders.processed_timestamp",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "description": "Data is available within 25 hours after the order was placed",
                "threshold": "25h",
                "source_timestamp_field": "orders.order_timestamp",
                "processed_timestamp_field": "orders.processed_timestamp",
            }
        }
    )


class FreshnessObject(BaseModel):
    """
    Represents the freshness service level for a data contract.

    This class defines the structure for the 'freshness' section of service levels,
    including details about the maximum age of the youngest entry.
    """

    description: Optional[str] = Field(
        None,
        description="A description of the freshness service level.",
        example="The age of the youngest row in a table.",
    )
    threshold: Optional[str] = Field(
        None,
        description="Maximum age of the youngest entry.",
        example="25h",
    )
    timestamp_field: Optional[str] = Field(
        None,
        description="Reference to the field containing the relevant timestamp.",
        example="orders.order_timestamp",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "description": "The age of the youngest row in a table.",
                "threshold": "25h",
                "timestamp_field": "orders.order_timestamp",
            }
        }
    )


class FrequencyObject(BaseModel):
    """
    Represents the frequency service level for a data contract.

    This class defines the structure for the 'frequency' section of service levels,
    including details about how often data is updated.
    """

    description: Optional[str] = Field(
        None,
        description="A description of the frequency service level.",
        example="Data is delivered once a day",
    )
    type: Optional[str] = Field(
        None,
        description="Type of data processing (e.g., 'batch', 'streaming').",
        example="batch",
    )
    interval: Optional[str] = Field(
        None,
        description="How often the pipeline is triggered (for batch processing).",
        example="daily",
    )
    cron: Optional[str] = Field(
        None,
        description="Cron expression for when the pipeline is triggered.",
        example="0 0 * * *",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "description": "Data is delivered once a day",
                "type": "batch",
                "interval": "daily",
                "cron": "0 0 * * *",
            }
        }
    )


class SupportObject(BaseModel):
    """
    Represents the support service level for a data contract.

    This class defines the structure for the 'support' section of service levels,
    including details about support availability and response times.
    """

    description: Optional[str] = Field(
        None,
        description="A description of the support service level.",
        example="The data is available during typical business hours at headquarters",
    )
    time: Optional[str] = Field(
        None,
        description="Times when support is available (e.g., '24/7', 'business hours').",
        example="9am to 5pm in EST on business days",
    )
    response_time: Optional[str] = Field(
        None, description="Expected time for support to acknowledge a request.", example="1h"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "description": "The data is available during typical business hours at headquarters",
                "time": "9am to 5pm in EST on business days",
                "response_time": "1h",
            }
        }
    )


class BackupObject(BaseModel):
    """
    Represents the backup service level for a data contract.

    This class defines the structure for the 'backup' section of service levels,
    including details about data backup procedures and recovery objectives.
    """

    description: Optional[str] = Field(
        None,
        description="A description of the backup service level.",
        example="Data is backed up once a week, every Sunday at 0:00 UTC.",
    )
    interval: Optional[str] = Field(
        None,
        description="How often data will be backed up.",
        example="weekly",
    )
    cron: Optional[str] = Field(
        None,
        description="Cron expression for when data will be backed up.",
        example="0 0 * * 0",
    )
    recovery_time: Optional[str] = Field(
        None,
        description="Maximum time allowed to restore data from a backup.",
        example="24 hours",
    )
    recovery_point: Optional[str] = Field(
        None,
        description="Maximum acceptable age of files for recovery.",
        example="1 week",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "description": "Data is backed up once a week, every Sunday at 0:00 UTC.",
                "interval": "weekly",
                "cron": "0 0 * * 0",
                "recovery_time": "24 hours",
                "recovery_point": "1 week",
            }
        }
    )


class ServiceLevelsObject(BaseModel):
    """
    Represents the service levels for a data contract.

    This class defines various service level attributes such as availability,
    retention, latency, freshness, frequency of data delivery, support, and backup.
    """

    availability: Optional[AvailabilityObject] = Field(None, description="Availability service level.")
    retention: Optional[RetentionObject] = Field(None, description="Data retention service level.")
    latency: Optional[LatencyObject] = Field(None, description="Latency service level.")
    freshness: Optional[FreshnessObject] = Field(None, description="Data freshness service level.")
    frequency: Optional[FrequencyObject] = Field(None, description="Data delivery frequency service level.")
    support: Optional[SupportObject] = Field(None, description="Support service level.")
    backup: Optional[BackupObject] = Field(None, description="Backup service level.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "availability": AvailabilityObject.model_config["json_schema_extra"]["example"],
                "retention": RetentionObject.model_config["json_schema_extra"]["example"],
                "latency": LatencyObject.model_config["json_schema_extra"]["example"],
                "freshness": FreshnessObject.model_config["json_schema_extra"]["example"],
                "frequency": FrequencyObject.model_config["json_schema_extra"]["example"],
                "support": SupportObject.model_config["json_schema_extra"]["example"],
                "backup": BackupObject.model_config["json_schema_extra"]["example"],
            }
        }
    )
