from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client.get_default_database()

@app.get("/ping")
async def ping():
    return {"msg": "pong"}
