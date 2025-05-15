from fastapi import FastAPI
from db.base import db
from models import Trademark
from api.main import api_router

app = FastAPI(title="MarkCloud 백엔드 개발자 과제 API", description="지원자 배성욱이 구현한 MarkCloud 백엔드 개발자 과제 API입니다.")

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"배성욱의 MarkCloud 백엔드 개발자 채용과제 API입니다!"}

