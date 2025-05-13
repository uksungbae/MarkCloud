from models.models import Trademark
from db.base import db
from bson.objectid import ObjectId
from typing import Optional

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