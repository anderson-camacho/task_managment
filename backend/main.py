from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from routers import auth, tasks
from bson import ObjectId
from datetime import datetime
from typing import List
from schemas.task import TaskCreate, TaskOut
from dependencies import get_current_user, get_database  # import explícito
from datetime import datetime, timezone

# Importar y montar routers
from routers.auth import router as auth_router
from routers.tasks import router as tasks_router

load_dotenv()

app = FastAPI()
app.include_router(auth.router)
app.include_router(tasks.router)

client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
app.mongodb = client["gestor_tareas"] 

def get_current_timestamp():
    return datetime.now(timezone.utc).isoformat()

@app.get("/ping")
async def ping():
    return {"timestamp": get_current_timestamp()}


router = APIRouter(prefix="/tasks", tags=["tasks"])

# Obtén la base de datos inyectada
@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    user=Depends(get_current_user),
    db=Depends(get_database)
):
    doc = task.dict()
    doc.update({
        "user_id": ObjectId(user["id"]),
        "status": "Pendiente",
        "created": datetime.utcnow()
    })
    result = await db.tasks.insert_one(doc)
    return TaskOut(**doc, id=str(result.inserted_id))
