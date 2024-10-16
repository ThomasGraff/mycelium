from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class TermObject(BaseModel):
    """
    Represents the terms and conditions of a data contract.

    This class defines the structure for the 'terms' section of a data contract,
    including details such as usage terms, limitations, billing information, and notice period.
    """

    usage: Optional[str] = Field(
        None,
        description="The way the data is expected to be used. Can contain business and technical information.",
        example="Data can be used for reports, analytics and machine learning use cases.",
    )
    limitations: Optional[str] = Field(
        None,
        description="Restrictions on how the data can be used, including technical limitations or usage restrictions.",
        example="Not suitable for real-time use cases. Data may not be used to identify individual customers.",
    )
    billing: Optional[str] = Field(
        None,
        description="The pricing model for using the data (e.g., free, monthly fee, or metered pay-per-use).",
        example="5000 USD per month",
    )
    notice_period: Optional[str] = Field(
        None,
        description="Period of time required to terminate or modify the data usage agreement. Uses ISO-8601 format.",
        example="P3M",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "usage": "Data can be used for reports, analytics and machine learning use cases.",
                "limitations": "Not suitable for real-time use cases. Data may not be used to identify individual customers.",
                "billing": "5000 USD per month",
                "notice_period": "P3M",
            }
        }
    )


def extract_pydantic_data() -> Dict[str, Any]:
    """
    Extracts detailed data from the TermObject Pydantic model and formats it for nice UI display.

    :return Dict[str, Any]: A dictionary containing formatted information about the model.
    """
    print("💡 Extracting and formatting data from TermObject Pydantic model")

    schema = TermObject.model_json_schema()
    fields_info = []

    for field_name, field in TermObject.model_fields.items():
        field_info = f"""
        Field: {field_name}
        ├─ Type: {str(field.annotation)}
        ├─ Required: {"✅" if field.is_required() else "❌"}
        ├─ Default: {field.default if field.default is not None else "N/A"}
        ├─ Description: {field.description}
        └─ Example: {field.json_schema_extra.get("example") if field.json_schema_extra else "N/A"}
        """
        fields_info.append(field_info.strip())

    formatted_fields = "\n\n".join(fields_info)

    return {
        "name": schema["title"],
        "docstring": TermObject.__doc__,
        "fields_display": f"""
        Model: {schema["title"]}

        Description:
        {TermObject.__doc__.strip()}

        Fields:
        {formatted_fields}
        """.strip(),
    }


print(extract_pydantic_data()["fields_display"])
