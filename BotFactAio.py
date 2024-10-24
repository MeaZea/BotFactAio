from flask import Flask, request
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.utils.executor import start_polling
import randfacts
from googletrans import Translator
from config import BOT_TOKEN  # Import the token from config.py

app = Flask(__name__)
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)
translator = Translator()

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text="Случайный факт")
keyboard.add(button_1)

def save_message(user_id, message_text, filename='messages.txt'):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"User ID: {user_id}, Message: {message_text}\n")

@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    await message.answer('Привет!\nЯ умею генерировать и отправлять случайные факты! Нажми или напиши /start для начала или обновления кнопки', reply_markup=keyboard)

@dp.message_handler(text='Случайный факт')
async def randfact(message: Message):
    save_message(message.from_user.id, message.text, 'facts_messages.txt')
    f = randfacts.get_fact(False)
    translation = translator.translate(f, dest='ru')
    await bot.send_message(message.from_user.id, translation.text)

@dp.message_handler()
async def handle_message(message: Message):
    save_message(message.from_user.id, message.text, 'general_messages.txt')
    await message.answer('Сообщение принято')

@app.route('/')
def index():
    return "Bot is running"

if __name__ == '__main__':
    start_polling(dp)
    app.run(host='0.0.0.0', port=10000)