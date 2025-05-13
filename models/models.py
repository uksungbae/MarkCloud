from pydantic import BaseModel, Field
from typing import Optional, List
from .objectID import PyObjectId  

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
