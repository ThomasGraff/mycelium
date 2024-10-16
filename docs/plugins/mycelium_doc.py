from __future__ import annotations

import ast
from typing import Any, Dict

from griffe import Class, Docstring, Extension, Inspector
from griffe import Object as GriffeObject
from griffe import ObjectNode, Visitor, get_logger
from pydantic import Field

logger = get_logger("mycelium_doc")


def extract_field_info(field: Field) -> Dict[str, Any]:
    """
    Extracts information from a Pydantic Field.

    :param Field field: The Pydantic Field to extract information from.
    :return Dict[str, Any]: A dictionary containing the field's description, type, and example.
    """
    return {
        "description": field.field_info.description or "No description",
        "type": str(field.outer_type_),
        "example": field.field_info.extra.get("example", "No example"),
        "default": field.default,
        "required": field.required,
    }


class PydanticFieldExtractorExtension(Extension):
    def on_instance(
        self,
        *,
        node: ast.AST | ObjectNode,
        obj: GriffeObject,
        agent: Visitor | Inspector,
        **kwargs: Any,
    ) -> None:
        """
        Adds docstrings to each field of Pydantic models.

        :param node: The AST node or object node.
        :param obj: The Griffe object representing the Pydantic model.
        :param agent: The visitor or inspector agent.
        """
        if isinstance(obj, Class) and not obj.is_alias:
            if self.inherits_pydantic(obj):
                logger.info("🔍 Processing Pydantic model: %s", obj.name)
                self.process_class(obj)

    def inherits_pydantic(self, cls: Class) -> bool:
        """
        Check if a class inherits from Pydantic BaseModel.

        :param cls: A Griffe class.
        :return: True if the class inherits from Pydantic BaseModel, False otherwise.
        """
        for base in cls.bases:
            if base.name == "BaseModel":
                return True
        return False

    def process_class(self, cls: Class) -> None:
        """
        Process a Pydantic model class.

        :param cls: The Griffe class object representing the Pydantic model.
        """
        fields_info = []
        for field_name, field in cls.attributes.items():
            if isinstance(field, GriffeObject):
                logger.info(f"🏷️  Processing field: {field_name}")
                field_info = extract_field_info(field)
                fields_info.append({"name": field_name, **field_info})
                self.process_attribute(field, cls)

        self.generate_class_docstring(cls, fields_info)

    def process_attribute(self, attr: GriffeObject, cls: Class) -> None:
        """
        Process a Pydantic field attribute.

        :param attr: The Griffe object representing the field.
        :param cls: The parent Pydantic model class.
        """
        attr.labels = {"pydantic-field"}
        constraints = {k: v for k, v in attr.value.items() if k not in {"default", "description"}}
        attr.extra["pydantic"] = {"constraints": constraints}

        if not attr.docstring and (docstring := attr.value.get("description")):
            attr.docstring = Docstring(ast.literal_eval(docstring), parent=attr)

    def generate_class_docstring(self, cls: Class, fields_info: list[dict]) -> None:
        """
        Generate a table-like docstring for the Pydantic model class.

        :param cls: The Griffe class object representing the Pydantic model.
        :param fields_info: List of dictionaries containing field information.
        """
        class_docstring = "| Field | Type | Description | Default | Required | Example |\n"
        class_docstring += "|-------|------|-------------|---------|----------|---------|\n"
        for field in fields_info:
            class_docstring += (
                f"| {field['name']} | `{field['type']}` | {field['description']} | "
                f"{field['default']} | {'Yes' if field['required'] else 'No'} | {field['example']} |\n"
            )

        cls.docstring = Docstring(class_docstring.strip(), parent=cls)
        logger.info(f"✅ Added table-like docstring to class: {cls.name}")

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
                    logger.info(f"💡 Added example from model_config for class: {cls.name}")
