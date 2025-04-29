from typing import Any, List

from pydantic import BaseModel, Field, field_validator

from .custom_types import RDczState


class RDczDocument(BaseModel):
    issue_id: str = Field(alias="id")
    record_id: int = Field(alias="titul_id")

    barcode: str = Field(alias="carkod")
    control_number: str = Field(alias="pole001")
    nbn: str | None = Field(None, alias="cnb")
    isxn: List[str] | None = Field(None, alias="isxn")
    signature: str | None = Field(None, alias="signatura")

    title: str
    volume_year: str | None = Field(None, alias="rozsah")
    volume_number: str | None = Field(None, alias="cast")
    bundle: str | None = Field(None, alias="cisloper")

    state: RDczState | None = Field(..., alias="stav")
    record_state: List[RDczState] = []

    @field_validator("state", mode="before")
    def validate_state(cls, value: Any):
        if isinstance(value, str):
            return RDczState.from_alias(value)

        return value

    @field_validator("record_state", mode="before")
    def validate_record_state(cls, value: Any):
        if isinstance(value, list):
            return [RDczState.map_from(v) for v in value]

        return value
