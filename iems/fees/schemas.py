from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date
from enum import Enum


class PaymentTypeEnum(str, Enum):
    CHEQUE = "cheque"
    UPI = "upi"
    NEFT = "neft"
    RTGS = "rtgs"
    OTHERS = "others"


class FeesTypeEnum(str, Enum):
    TUTION_FEES = "tution_fees"
    EXAM_FEES = "exam_fees"
    CARD_FEES = "card_fees"
    OTHERS = "others"


class CreateFeesRequest(BaseModel, use_enum_values=True):
    date: date
    student_id: str
    type: FeesTypeEnum
    payment_type: PaymentTypeEnum
    transaction_id: str = Field(..., max_length=128)
    amount: float = Field(..., gt=0)
    docs_uuid:Optional[UUID]=None
    status:str = "PENDING"


class CreateFeesResponse(BaseModel):
    id: UUID
    recipt_id: int


class GetFeesResponse(BaseModel):
    id: UUID
    recipt_id: int
    date: date
    student_id: UUID
    enrollment_id: str
    type: FeesTypeEnum
    payment_type: PaymentTypeEnum
    transaction_id: str
    amount: float
    docs_uuid:Optional[UUID]
    status:str = "PENDING"


class GetFeesByStudentResponse(BaseModel):
    fees: list[GetFeesResponse]


class UpdateFeesRequest(BaseModel):
    date: date
    type: FeesTypeEnum
    payment_type: PaymentTypeEnum
    transaction_id: str = Field(max_length=128)
    amount: float = Field(gt=0)

class UpdateFeesStatusRequest(BaseModel):
    accepted: bool


class FeesNotFoundResponse(BaseModel):
    error: str = "fees_not_found"
    message: str = "Fees record not found"


class EmptyResponse(BaseModel): ...
