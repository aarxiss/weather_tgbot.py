import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

API_TOKEN = "..."
WEATHER_API_KEY = "..."

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    # Відправляємо без HTML, щоб уникнути помилки з тегами
    await message.answer("Привіт! Введи /weather місто, щоб дізнатися погоду.")

@dp.message(Command("help"))
async def help_handler(message: Message):
    text = (
        "/start — почати роботу з ботом\n"
        "/help — список команд\n"
        "/info — інформація про бота\n"
        "/exit — завершити роботу\n"
        "/weather <місто> — погода у вказаному місті"
    )
    await message.answer(text)

@dp.message(Command("info"))
async def info_handler(message: Message):
    await message.answer("Це асинхронний Telegram-бот на aiogram v3, який показує погоду через OpenWeather API.")

@dp.message(Command("exit"))
async def exit_handler(message: Message):
    await message.answer("Дякую, що скористалися ботом! Бувай 👋")

@dp.message(Command("weather"))
async def weather_handler(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Вкажи місто після команди, наприклад:\n/weather Kyiv")
        return

    city = args[1]

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=uk"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await message.answer("Не вдалося отримати дані про погоду. Перевірте назву міста.")
                return
            data = await resp.json()

    weather_desc = data['weather'][0]['description'].capitalize()
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    response = (
        f"Погода в <b>{city.title()}</b>:\n"
        f"{weather_desc}\n"
        f"Температура: {temp}°C (відчувається як {feels_like}°C)\n"
        f"Вологість: {humidity}%\n"
        f"Швидкість вітру: {wind_speed} м/с"
    )

    await message.answer(response)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
