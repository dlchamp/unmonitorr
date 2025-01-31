from pydantic import BaseModel, ConfigDict

__all__ = ("SharedBaseModel",)


def _to_camel_case(string: str) -> str:
    """Convert snake_case to camelCase."""
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class SharedBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=_to_camel_case,
        populate_by_name=True,
        from_attributes=True,
        extra="allow",
    )
