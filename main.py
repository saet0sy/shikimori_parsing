import logging
import json
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import Message
from aiogram import executor
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app import scrape_anime
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = '6278066311:AAHgHZVijYF5eqMfnKkh8JXXvKrHjLplkOU'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

with open('products.json', 'r', encoding='utf-8') as f:
    anime_list = json.load(f)

users_chat_ids = set()

def get_random_anime():
    if not anime_list:
        return "К сожалению, список аниме пуст."
    random_anime = random.choice(anime_list)
    return random_anime['title']

async def send_random_anime():
    while True:
        await asyncio.sleep(3)
        random_anime = get_random_anime()
        for chat_id in users_chat_ids:
            await bot.send_message(chat_id=chat_id, text=f"Рандомное аниме: {random_anime}")

# /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_anime = KeyboardButton('/anime')
    button_stop = KeyboardButton('/stop')
    keyboard.add(button_anime, button_stop)
    
    await message.answer("Привет! Я бот! Нажми кнопку '/anime', чтобы получить рандомное аниме.", reply_markup=keyboard)

    users_chat_ids.add(message.chat.id)

class IsSending(StatesGroup):
    sending = State()

# /anime
@dp.message_handler(commands=['anime', '/anime']) 
async def cmd_anime(message: Message):
    random_anime = get_random_anime()
    await message.answer(f"Рандомное аниме: {random_anime}")

# stop

@dp.message_handler(commands=['stop', '/stop'])
async def cmd_stop(message: Message):
    await message.answer("Спасибо за пользование ботоМ! До свидания!")
    users_chat_ids.remove(message.chat.id)

# /users
@dp.message_handler(commands=['users'])
async def cmd_users(message: Message):
    users = ", ".join(str(chat_id) for chat_id in users_chat_ids)
    await message.answer(f"Список пользователей: {users}")

# messages
@dp.message_handler()
async def echo_message(message: Message):
    await message.answer(f"Вы написали: {message.text}")

async def on_startup(dp):
    print("Bot started.")
    print("Users in chat_ids:", users_chat_ids)
    asyncio.create_task(send_random_anime())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
