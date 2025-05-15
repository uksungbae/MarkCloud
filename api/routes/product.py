from models.models import Trademark, TrademarkSearchParams, RegisterStatus
from fastapi import APIRouter, Path, HTTPException
from crud import get_product as crud_get_product
from crud import get_trademarks
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
