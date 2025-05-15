from models.models import Trademark, AdvancedSearchParams
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



async def search_similar_trademarks(params: AdvancedSearchParams) -> List[Dict]:
    """
    Atlas Search를 사용한 유사 키워드 검색
    """
    try:
        # 검색 pipeline 구성
        pipeline = [
            {
                "$search": {
                    "index": "markcloudSearch",  # Atlas에서 생성한 인덱스 이름
                    "compound": {
                        "should": [
                            {
                                "text": {
                                    "query": params.searchTerm,
                                    "path": params.fields,
                                    "fuzzy": {
                                        "maxEdits": 2 if params.fuzzySearch else 0,
                                        "prefixLength": 1
                                    },
                                    "score": {"boost": {"value": 3}}
                                }
                            },
                            # 추가 검색 옵션 - 동의어 옵션은 일단 비활성화
                            {
                                "text": {
                                    "query": params.searchTerm,
                                    "path": params.fields,
                                    "score": {"boost": {"value": 2}}
                                }
                            },
                        ]
                    }
                }
            },
            # 관련성 점수와 함께 반환
            {
                "$project": {
                    "_id": 1,
                    "productName": 1,
                    "productNameEng": 1,
                    "applicationNumber": 1,
                    "registerStatus": 1,
                    "score": {"$meta": "searchScore"}
                }
            },
            # 높은 점수 순으로 정렬
            {
                "$sort": {"score": -1}
            },
            # 결과 제한
            {
                "$limit": 10
            }
        ]
        
        # 파이프라인 실행
        cursor = db.trademark_sample.aggregate(pipeline)
        results = await cursor.to_list(length=100)
        
        # ObjectId 직렬화 문제 해결
        for result in results:
            if "_id" in result and isinstance(result["_id"], ObjectId):
                result["_id"] = str(result["_id"])
                
        # 최소 점수 필터링
        filtered_results = []
        for result in results:
            if "score" in result and result["score"] >= params.minScore:
                filtered_results.append(result)
                
        return filtered_results
    
    except Exception as e:
        # Atlas Search 오류 발생 시 에러 메시지만 출력
        print(f"Atlas Search error: {str(e)}")
        # 빈 결과 반환
        return []