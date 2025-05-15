from models.models import Trademark, TrademarkSearchParams, RegisterStatus, AdvancedSearchParams
from fastapi import APIRouter, Path, HTTPException
from crud import get_product as crud_get_product
from crud import get_trademarks, search_similar_trademarks
from fastapi import Depends
from typing import List
from typing import Dict
from db.base import db

router = APIRouter(prefix="/products", tags=["products"])




@router.get("/{product_id}", response_model=Trademark)
async def get_product_by_id(
    product_id: str = Path(..., description="조회할 상표 ID")
):
    """
    상표 ID로 단일 상표 데이터 조회
    """
    product = await crud_get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product



@router.get("/", response_model=List[Trademark])
async def search_trademarks(
    search_params: TrademarkSearchParams = Depends()
):
    """
    상표 데이터 검색 API (필터링)

    """
    results = await get_trademarks(filters=search_params.model_dump())
    return results

@router.get("/status/counts", response_model=Dict[str, int])
async def get_status_counts():
    """
    상표 등록 상태별 개수 조회
    """
    statuses = [status.value for status in RegisterStatus]
    result = {}
    
    for status in statuses:
        count = await db.trademark_sample.count_documents({"registerStatus": status})
        result[status] = count
    
    return result


@router.post("/search/similar", response_model=List[Dict])
async def find_similar_trademarks(
    search_params: AdvancedSearchParams
):
    """
    유사 키워드 기반 상표 검색 API
    - fuzzySearch: 퍼지 검색 활성화 여부 (오타 허용)
    - synonym: 동의어 검색 활성화 여부
    - minScore: 최소 유사도 점수 (0.0-1.0)
    """
    # 검색 요청 파라미터 출력
    print(f"Searching for: {search_params.searchTerm}, fuzzy: {search_params.fuzzySearch}, min score: {search_params.minScore}")
    
    # 최소 점수 값 조정 (0.5가 너무 높을 수 있음)
    search_params.minScore = 0.1  # 기본값이 업데이트되지 않을 경우 대비
    
    results = await search_similar_trademarks(search_params)
    
    # 결과가 없으면 최소 점수를 더 낮어서 다시 시도
    if not results:
        print("No results found with current settings, trying with lower score threshold...")
        search_params.minScore = 0.01
        results = await search_similar_trademarks(search_params)
        
    print(f"Found {len(results)} results")
    return results