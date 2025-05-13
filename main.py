from fastapi import FastAPI
from db.base import db
from models import Trademark
from api.main import api_router

app = FastAPI()

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


# db 조회 테스트
@app.get("/trademarks/", response_model=list[Trademark])
async def get_all_trademarks():
    cursor = db.trademark_sample.find()
    results = await cursor.to_list(length=10) 
    return results
