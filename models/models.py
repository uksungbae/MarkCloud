from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from .utils import PyObjectId

class Trademark(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    productName: Optional[str] = None
    productNameEng: Optional[str] = None
    applicationNumber: Optional[str] = None
    applicationDate: Optional[str] = None
    registerStatus: Optional[str] = None
    publicationNumber: Optional[str] = None
    publicationDate: Optional[str] = None
    registrationNumber: Optional[List[str]] = None
    registrationDate: Optional[List[Optional[str]]] = None
    registrationPubNumber: Optional[str] = None
    registrationPubDate: Optional[str] = None
    internationalRegDate: Optional[str] = None
    internationalRegNumbers: Optional[List[str]] = None
    priorityClaimNumList: Optional[List[str]] = None
    priorityClaimDateList: Optional[List[str]] = None
    asignProductMainCodeList: Optional[List[str]] = None
    asignProductSubCodeList: Optional[List[str]] = None
    viennaCodeList: Optional[List[str]] = None


class RegisterStatus(str, Enum):
    """상표 등록 상태 열거형"""
    REGISTERED = "등록"
    EXPIRED = "실효"
    REJECTED = "거절"
    APPLIED = "출원"

class TrademarkSearchParams(BaseModel):
    """상표 검색 필터링 파라미터"""
    productName: Optional[str] = None
    productNameEng: Optional[str] = None
    applicationNumber: Optional[str] = None
    applicationDateFrom: Optional[str] = None
    applicationDateTo: Optional[str] = None
    registerStatus: Optional[RegisterStatus] = None
    mainCode: Optional[str] = None
    subCode: Optional[str] = None
    viennaCode: Optional[str] = None
