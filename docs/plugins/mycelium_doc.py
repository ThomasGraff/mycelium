"""Griffe extension for Pydantic field extraction and documentation."""

from __future__ import annotations

import ast
from typing import Any, Optional

from griffe import Class, Docstring, Extension, Inspector
from griffe import Object as GriffeObject
from griffe import ObjectNode, Visitor, get_logger
from pydantic import BaseModel, Field

logger = get_logger(__name__)


class FieldInfo(BaseModel):
    """Represents the extracted information from a Pydantic Field."""

    name: str
    type: str
    description: Optional[str] = None
    required: bool = False
    default: Any = None
    example: Any = None


def extract_field_info(field_name: str, field: Field) -> FieldInfo:
    """
    Extracts information from a Pydantic Field.

    :param str field_name: The name of the field.
    :param Field field: The Pydantic Field to extract information from.
    :return FieldInfo: An object containing the field's information.
    """
    return FieldInfo(
        name=field_name,
        description=field.field_info.description or "No description",
        type=str(field.outer_type_),
        example=field.field_info.extra.get("example", "No example"),
        default=field.default,
        required=field.required,
    )


class PydanticFieldExtractorExtension(Extension):
    """Griffe extension for extracting and documenting Pydantic fields."""

    def __init__(self) -> None:
        """Initialize the extension."""
        super().__init__()
        self.in_model: list[Class] = []
        self.processed: set[str] = set()

    def on_instance(
        self,
        *,
        node: ast.AST | ObjectNode,
        obj: GriffeObject,
        agent: Visitor | Inspector,
        **kwargs: Any,
    ) -> None:
        """
        Process Pydantic model instances.

        :param node: The AST node or object node.
        :param obj: The Griffe object representing the Pydantic model.
        :param agent: The visitor or inspector agent.
        """
        if isinstance(obj, Class) and not obj.is_alias:
            if self.inherits_pydantic(obj):
                logger.info("🔍 Processing Pydantic model: %s", obj.name)
                self.in_model.append(obj)
                self.process_class(obj)
                self.processed.add(obj.canonical_path)

    def inherits_pydantic(self, cls: Class) -> bool:
        """
        Check if a class inherits from Pydantic BaseModel.

        :param cls: A Griffe class.
        :return: True if the class inherits from Pydantic BaseModel, False otherwise.
        """
        return any(base.name == "BaseModel" for base in cls.bases)

    def process_class(self, cls: Class) -> None:
        """
        Process a Pydantic model class.

        :param cls: The Griffe class object representing the Pydantic model.
        """
        for field_name, field in cls.attributes.items():
            if isinstance(field, GriffeObject):
                logger.info("🏷️  Processing field: %s", field_name)
                field_info = extract_field_info(field_name, field)
                self.process_attribute(field, field_info)

        self.process_model_config(cls)

    def process_attribute(self, attr: GriffeObject, field_info: FieldInfo) -> None:
        """
        Process a Pydantic field attribute.

        :param attr: The Griffe object representing the field.
        :param field_info: FieldInfo object containing field information.
        """
        attr.labels = {"pydantic-field"}
        constraints = {k: v for k, v in attr.value.items() if k not in {"default", "description"}}
        attr.extra["pydantic"] = {"constraints": constraints}

        field_docstring = (
            f"Represents the {field_info.name} field.\n\n"
            f"Type: {field_info.type}\n"
            f"Required: {'Yes' if field_info.required else 'No'}\n"
            f"Default: {field_info.default if field_info.default is not None else 'N/A'}\n"
            f"Description: {field_info.description}\n"
            f"Example: {field_info.example}\n"
        )

        attr.docstring = Docstring(field_docstring.strip(), parent=attr)
        logger.info("✅ Added detailed docstring to field: %s", field_info.name)

    def process_model_config(self, cls: Class) -> None:
        """
        Process the model_config attribute of a Pydantic model.

        :param cls: The Griffe class object representing the Pydantic model.
        """
        if "model_config" in cls.attributes:
            config = cls.attributes["model_config"]
            if isinstance(config, GriffeObject):
                extra_schema = config.value.get("json_schema_extra", {})
                if "example" in extra_schema:
                    cls.extra["pydantic_example"] = extra_schema["example"]
                    logger.info("💡 Added example from model_config for class: %s", cls.name)

    def on_class_members(self, *, node: ast.AST | ObjectNode, cls: Class, **kwargs: Any) -> None:
        """
        Finalize the Pydantic model data.

        :param node: The AST node or object node.
        :param cls: The Griffe class object.
        """
        if not isinstance(node, ast.AST) and self.in_model and cls is self.in_model[-1]:
            self.in_model.pop()
