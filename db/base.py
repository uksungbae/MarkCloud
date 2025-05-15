import certifi
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging

# 로거 설정
logger = logging.getLogger(__name__)

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

client = AsyncIOMotorClient(MONGODB_URI, tlsCAFile=certifi.where())
db = client[DB_NAME]


try:
    client.admin.command("ping")
    logger.info("MongoDB 연결 성공")
except Exception as e:
    logger.error("MongoDB 연결 실패:", e)
