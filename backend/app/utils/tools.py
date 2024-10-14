from ..models.data_contract import DataContract as DBDataContract
from ..schemas.data_contract.data_contract import DataContract as PydanticDataContract


def pydantic_to_db_model(pydantic_model: PydanticDataContract) -> DBDataContract:
    """
    Converts a Pydantic DataContract model to a SQLAlchemy DataContract model.

    :param PydanticDataContract pydantic_model: The Pydantic model to convert.
    :return DBDataContract: The corresponding SQLAlchemy model.
    """
    db_model = DBDataContract(
        id=pydantic_model.id,
        data_contract_specification=pydantic_model.data_contract_specification,
        info_title=pydantic_model.info.title,
        info_version=pydantic_model.info.version,
        info_description=pydantic_model.info.description,
        info_owner=pydantic_model.info.owner,
        info_contact=pydantic_model.info.contact.model_dump() if pydantic_model.info.contact else None,
        servers=(
            [server.model_dump() for server in pydantic_model.servers.values()] if pydantic_model.servers else None
        ),
        terms=pydantic_model.terms.model_dump() if pydantic_model.terms else None,
        models={k: v.model_dump() for k, v in pydantic_model.models.items()} if pydantic_model.models else None,
        examples=[example.model_dump() for example in pydantic_model.examples] if pydantic_model.examples else None,
        service_levels=pydantic_model.service_levels.model_dump() if pydantic_model.service_levels else None,
        links={str(k): str(v) for k, v in pydantic_model.links.items()} if pydantic_model.links else None,
        tags=pydantic_model.tags,
    )
    return db_model


def db_to_pydantic_model(db_model: DBDataContract) -> PydanticDataContract:
    """
    Converts a SQLAlchemy DataContract model to a Pydantic DataContract model.

    :param DBDataContract db_model: The SQLAlchemy model to convert.
    :return PydanticDataContract: The corresponding Pydantic model.
    """
    # Convert the SQLAlchemy model to a dictionary
    db_dict = {c.name: getattr(db_model, c.name) for c in db_model.__table__.columns}

    # Reconstruct the nested structures
    info = {
        "title": db_dict["info_title"],
        "version": db_dict["info_version"],
        "description": db_dict["info_description"],
        "owner": db_dict["info_owner"],
        "contact": db_dict["info_contact"],
    }
    db_dict["info"] = info

    # Remove the individual info fields
    for key in ["info_title", "info_version", "info_description", "info_owner", "info_contact"]:
        db_dict.pop(key, None)

    # Convert servers back to a dictionary if it exists
    if db_dict.get("servers"):
        db_dict["servers"] = {f"server_{i}": server for i, server in enumerate(db_dict["servers"])}

    # Use Pydantic's model_validate to create the Pydantic model
    return PydanticDataContract.model_validate(db_dict)
