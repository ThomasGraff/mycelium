from typing import Dict, List, Optional

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, HttpUrl

from .example_object import ExampleObject
from .info_object import InfoObject
from .model_object import ModelObject
from .server_object import ServerObject
from .service_level_object import ServiceLevelsObject
from .term_object import TermsObject


class DataContract(BaseModel):
    """
    Represents a Data Contract following the specifications from datacontract.com.

    :param str data_contract_specification: REQUIRED. Specifies the Data Contract Specification being used.
    :param str id: REQUIRED. An organization-wide unique technical identifier.
    :param InfoObject info: REQUIRED. Specifies the metadata of the data contract.
    :param Dict[str, ServerObject] servers: Specifies the servers of the data contract.
    :param TermsObject terms: Specifies the terms and conditions of the data contract.
    :param Dict[str, ModelObject] models: Specifies the logical data model.
    :param List[ExampleObject] examples: Specifies example data sets for the data model.
    :param ServiceLevelsObject service_levels: Specifies the service level of the provided data.
    :param Dict[str, HttpUrl] links: Additional external documentation links.
    :param List[str] tags: Custom metadata to provide additional context.
    """

    data_contract_specification: str = Field(
        ...,
        description="REQUIRED. Specifies the Data Contract Specification being used.",
        validation_alias=AliasChoices("data_contract_specification", "dataContractSpecification"),
    )
    id: str = Field(..., description="REQUIRED. An organization-wide unique technical identifier.")
    info: InfoObject = Field(..., description="REQUIRED. Specifies the metadata of the data contract.")
    servers: Optional[Dict[str, ServerObject]] = Field(None, description="Specifies the servers of the data contract.")
    terms: Optional[TermsObject] = Field(None, description="Specifies the terms and conditions of the data contract.")
    models: Optional[Dict[str, ModelObject]] = Field(None, description="Specifies the logical data model.")
    examples: Optional[List[ExampleObject]] = Field(
        None, description="Specifies example data sets for the data model."
    )
    service_levels: Optional[ServiceLevelsObject] = Field(
        None,
        description="Specifies the service level of the provided data.",
        validation_alias=AliasChoices("service_levels", "serviceLevels"),
    )
    links: Optional[Dict[str, HttpUrl]] = Field(None, description="Additional external documentation links.")
    tags: Optional[List[str]] = Field(None, description="Custom metadata to provide additional context.")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "dataContractSpecification": "0.9.3",
                "id": "urn:datacontract:checkout:orders-latest",
                "info": {
                    "title": "Orders Latest",
                    "version": "1.0.0",
                    "description": "Successful customer orders in the webshop.",
                    "owner": "Checkout Team",
                },
            }
        },
    )
