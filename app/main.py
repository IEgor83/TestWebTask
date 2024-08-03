import os
from fastapi import FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION = os.getenv("COLLECTION")

# Подключение к MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION]


class Message(BaseModel):
    id: str
    content: str


class MessageCreate(BaseModel):
    content: str


@app.get("/api/v1/messages/", response_model=List[Message])
async def get_messages():
    messages = []
    async for message in collection.find():
        messages.append(Message(id=str(message["_id"]), content=message["content"]))
    return messages


@app.post("/api/v1/message/", response_model=Message)
async def create_message(message: MessageCreate):
    new_message = {"content": message.content}
    result = await collection.insert_one(new_message)
    return Message(id=str(result.inserted_id), content=message.content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
