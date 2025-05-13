from models.models import Trademark
from fastapi import APIRouter, Path, HTTPException
from crud import get_product as crud_get_product

router = APIRouter(prefix="/api/products", tags=["products"])

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
