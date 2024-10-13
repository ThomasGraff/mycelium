from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ServiceLevelsObject(BaseModel):
    """
    Represents the service levels for a data contract.

    This class defines various service level attributes such as availability,
    retention, latency, freshness, and frequency of data delivery.
    """

    availability: Optional[Dict[str, Any]] = Field(None, description="Availability service level.")
    retention: Optional[Dict[str, Any]] = Field(None, description="Data retention service level.")
    latency: Optional[Dict[str, Any]] = Field(None, description="Latency service level.")
    freshness: Optional[Dict[str, Any]] = Field(None, description="Data freshness service level.")
    frequency: Optional[Dict[str, Any]] = Field(None, description="Data delivery frequency service level.")
