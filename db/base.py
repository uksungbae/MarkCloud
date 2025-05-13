import certifi
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

client = AsyncIOMotorClient(MONGODB_URI, tlsCAFile=certifi.where())
db = client[DB_NAME]


try:
    client.admin.command("ping")
    print("MongoDB 연결 성공")
except Exception as e:
    print("MongoDB 연결 실패:", e)
