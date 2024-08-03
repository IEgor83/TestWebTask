import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message as TgMessage
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# Конфигурация логирования
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Создание бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION = os.getenv("COLLECTION")

# Подключение к MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION]


@dp.message(Command("start"))
async def cmd_start(message: TgMessage):
    await message.answer("Добро пожаловать! Вы можете посмотреть сообщения командой /messages и создать сообщение "
                         "командой /new_message <ваше сообщение>")


@dp.message(Command("messages"))
async def get_messages(message: TgMessage):
    messages = []
    async for msg in collection.find():
        messages.append(f"{msg['_id']}: {msg['content']}")
    await message.answer("\n".join(messages) or "Сообщений пока нет")


@dp.message(Command("new_message"))
async def create_message(message: TgMessage):
    content = message.text[len("/new_message "):].strip()
    if content:
        new_message = {"content": content}
        result = await collection.insert_one(new_message)
        await message.answer(f"Сообщение добавлено с ID: {result.inserted_id}")
    else:
        await message.answer("Сообщение не должно быть пустым!")

if __name__ == "__main__":
    dp.run_polling(bot)
