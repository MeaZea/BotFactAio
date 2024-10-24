import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.utils.executor import start_webhook
import randfacts
from googletrans import Translator

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Чтение токена из переменной окружения
WEBHOOK_HOST = 'https://youraya_telebot.onrender.com'  # Замените на ваш домен на Render
WEBHOOK_PATH = '/webhook/' + BOT_TOKEN
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

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

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host='0.0.0.0',
        port=port,
    )