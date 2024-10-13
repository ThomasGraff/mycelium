from typing import Optional

from pydantic import BaseModel, Field


class TermsObject(BaseModel):
    """
    Represents the terms and conditions of a data contract.

    This class defines the structure for the 'terms' section of a data contract,
    including details such as usage terms, limitations, billing information, and notice period.
    """

    usage: Optional[str] = Field(None, description="Usage terms of the data contract.")
    limitations: Optional[str] = Field(None, description="Limitations of the data contract.")
    billing: Optional[str] = Field(None, description="Billing information for the data contract.")
    noticePeriod: Optional[str] = Field(None, description="Notice period for changes to the data contract.")
