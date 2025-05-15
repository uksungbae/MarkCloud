from models.models import Trademark, TrademarkSearchParams, RegisterStatus, AdvancedSearchParams
from fastapi import APIRouter, Path, HTTPException
from crud import get_product as crud_get_product
from crud import get_trademarks, search_similar_trademarks
from fastapi import Depends
from typing import List
from typing import Dict
from db.base import db
import logging

# 로거 설정
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/filter", response_model=List[Trademark])
async def search_trademarks(
    search_params: TrademarkSearchParams = Depends()
):
    """
    상표 데이터 검색 API (필터링)

    :상표 필터링을 위한 API
    
    parameter: 필드 전체 
    """
    results = await get_trademarks(filters=search_params.model_dump())
    return results


@router.get("/{product_id}", response_model=Trademark)
async def get_product_by_id(
    product_id: str = Path(..., description="조회할 상표 ID")
):
    """
    상표 ID(objectID)로 단일 상표 데이터 조회
    
    :상표 상세 페이지를 위한 API

    parameter: 조회할 상표 ID(mongoDB objectID)
    """
    product = await crud_get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/status/counts", response_model=Dict[str, int])
async def get_status_counts():
    """
    상표 등록 상태별 개수 조회 API
    
    no parameter
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
    유사 키워드 검색 API

    :Atlas Search를 적용한 상표 검색 API


    특징:

    -퍼지 검색: 오타를 허용하되 단어의 첫글자는 일치해야 함(prefixLength=1)

    -관련성 점수: 검색 결과는 관련성 점수에 따라 정렬됨

    -최소 점수 필터링: 낮은 관련성의 결과는 제외됨
    
    parameter:

    -searchTerm: 검색할 키워드

    -fields: 검색할 필드 목록(productName, productNameEng)

    -fuzzySearch: 퍼지 검색 활성화 여부(True)

    -minScore: 최소 관련성 점수(0.5)
    
    """
    # 검색 요청 로깅
    logger.info(f"Searching for: {search_params.searchTerm}, fuzzy: {search_params.fuzzySearch}, min score: {search_params.minScore}")
    
    # 최소 점수 값 조정 (0.5가 너무 높을 수 있음)
    search_params.minScore = 0.1  # 기본값이 업데이트되지 않을 경우 대비
    
    results = await search_similar_trademarks(search_params)
    
    # 결과가 없으면 최소 점수를 더 낮아서 다시 시도
    if not results:
        logger.warning("No results found with current settings, trying with lower score threshold...")
        search_params.minScore = 0.01
        results = await search_similar_trademarks(search_params)
        
    logger.info(f"Found {len(results)} results")
    return results