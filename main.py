from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

TELEGRAM_TOKEN = '6304485952:AAFNEYzZzRjj2vDmFbBvEQ3oSE_udHwxL54'
OWM_API_KEY = '1247a0c87048a85a5bf2c48333d3554a'

def get_weather(city: str) -> str:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=uk&appid={OWM_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city_name = data.get('name')
        temp = data['main']['temp']
        weather_desc = data['weather'][0]['description']
        return f"Погода в {city_name}: {temp}°C, {weather_desc.capitalize()}"
    else:
        return 'Не вдалося знайти інформацію про погоду. Перевірте назву міста.'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🌍 Передати геопозицію", request_location=True)]

    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text(
        'Привіт! Виберіть одну з опцій нижче, щоб дізнатись погоду',
        reply_markup=reply_markup
    )

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    lat = location.latitude
    lon = location.longitude
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=uk&appid={OWM_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city_name = data.get('name')
        temp = data['main']['temp']
        weather_desc = data['weather'][0]['description']
        await update.message.reply_text(f"Погода в {city_name}: {temp}°C, {weather_desc.capitalize()}")
    else:
        await update.message.reply_text("Не вдалося отримати погоду за вашою геопозицією.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    weather = get_weather(city)
    await update.message.reply_text(weather)

def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    application.run_polling()

if __name__ == '__main__':
    main()




