from models.models import Trademark
from db.base import db
from bson.objectid import ObjectId
from typing import Optional, List, Dict, Any

async def get_product(product_id: str) -> Optional[Trademark]:
    """
    상표 ID로 단일 상표 데이터 조회
    """
    if not ObjectId.is_valid(product_id):
        return None
    
    product = await db.trademark_sample.find_one({"_id": ObjectId(product_id)})
    if product:
        return Trademark(**product)
    return None



async def get_trademarks(
    filters: Dict[str, Any] = None
) -> List[Trademark]:
    """
    필터링으로 상표 데이터 조회 
    """
    query = {}
    
    # 필터 적용
    if filters:
        # 상표명 검색 (한글/영문)
        if filters.get("productName"):
            query["productName"] = {"$regex": filters["productName"], "$options": "i"}
        if filters.get("productNameEng"):
            query["productNameEng"] = {"$regex": filters["productNameEng"], "$options": "i"}
        
        # 출원번호 검색
        if filters.get("applicationNumber"):
            query["applicationNumber"] = filters["applicationNumber"]
        
        # 출원일 범위 검색
        if filters.get("applicationDateFrom") and filters.get("applicationDateTo"):
            query["applicationDate"] = {
                "$gte": filters["applicationDateFrom"],
                "$lte": filters["applicationDateTo"]
            }
        elif filters.get("applicationDateFrom"):
            query["applicationDate"] = {"$gte": filters["applicationDateFrom"]}
        elif filters.get("applicationDateTo"):
            query["applicationDate"] = {"$lte": filters["applicationDateTo"]}
        
        # 등록 상태 검색
        if filters.get("registerStatus"):
            query["registerStatus"] = filters["registerStatus"]
        
        # 상품 주 분류 코드 검색
        if filters.get("mainCode"):
            query["asignProductMainCodeList"] = {"$in": [filters["mainCode"]]}
        
        # 상품 유사군 코드 검색
        if filters.get("subCode"):
            query["asignProductSubCodeList"] = {"$in": [filters["subCode"]]}
        
        # 비엔나 코드 검색
        if filters.get("viennaCode"):
            query["viennaCodeList"] = {"$in": [filters["viennaCode"]]}
    
    cursor = db.trademark_sample.find(query)
    results = await cursor.to_list(length=10)
    return results