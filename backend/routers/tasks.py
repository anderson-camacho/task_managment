from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from bson import ObjectId
from datetime import datetime
from ..schemas.task import TaskCreate, TaskOut
from ..dependencies import get_current_user  # asume que ya existe esta dependencia

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, user=Depends(get_current_user)):
    doc = task.dict()
    doc.update({
        "user_id": ObjectId(user.id),
        "status": "Pendiente",
        "created": datetime.utcnow()
    })
    result = await router.mongodb.tasks.insert_one(doc)
    return TaskOut(**doc, id=str(result.inserted_id))

@router.get("/", response_model=List[TaskOut])
async def read_tasks(user=Depends(get_current_user)):
    cursor = router.mongodb.tasks.find({"user_id": ObjectId(user.id)})
    tasks = []
    async for d in cursor:
        tasks.append(TaskOut(**d, id=str(d["_id"])))
    return tasks

@router.put("/{task_id}", response_model=TaskOut)
async def update_task(task_id: str, task: TaskCreate, user=Depends(get_current_user)):
    oid = ObjectId(task_id)
    existing = await router.mongodb.tasks.find_one({"_id": oid, "user_id": ObjectId(user.id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    update_data = task.dict()
    update_data["updated"] = datetime.utcnow()
    await router.mongodb.tasks.update_one({"_id": oid}, {"$set": update_data})
    updated = {**existing, **update_data}
    return TaskOut(**updated, id=task_id)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, user=Depends(get_current_user)):
    oid = ObjectId(task_id)
    result = await router.mongodb.tasks.delete_one({"_id": oid, "user_id": ObjectId(user.id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return
