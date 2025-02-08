from typing import Any
from pydantic import BaseModel, Field


class ValidationError(BaseModel):
    type: str = Field(description="Cause of Data Invalidation")
    location: list[Any] = Field(description="Location at which the data is invalid")


class DataValidationExceptionModel(BaseModel):
    slug: str = "invalid_data"
    description: str = "Data is invalid"
    context: list[ValidationError] = Field(
        description="List of causes of data invalidation"
    )


class UnkownExceptionModel(BaseModel):
    slug: str = "unkown_error"
    description: str = "An unkown error occured"
