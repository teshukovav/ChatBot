import logging
import random
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Замените на ваш токен Telegram
TOKEN = '7322321899:AAHA2t4_iqyhwSzT185KtvsB8NLKJ3x-oi4'
GENIUS_ACCESS_TOKEN = 'TRySUhV85Rw76Pz1RZw9TFEYp5fxZdb9qRQmnT1T3kHOP9K3hq6jVsVDujhqsdyN'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Список роз
roses = [
    "🌹 Красная роза - символ любви и страсти",
    "🌸 Розовая роза - символ изящества и элегантности",
    "🥀 Увядающая роза - символ быстротечности красоты",
    "🌷 Тюльпановидная роза - символ совершенной любви",
    "💮 Белая роза - символ чистоты и невинности"
]

def get_keyboard():
    keyboard = [
        ['😊 Комплимент', '🎵 Песня'],
        ['🌞 Пожелание', '🌹 Показать розу'],
        ['❓ Помощь']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        'Привет! Я бот, который может сделать твой день лучше.',
        reply_markup=get_keyboard()
    )

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Выбери одну из опций на клавиатуре.')

async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text == '😊 Комплимент':
        await update.message.reply_text('Ты самый замечательный человек на свете!')
    elif text == '🎵 Песня':
        try:
            query = "happy"  # Замените на любое слово для поиска песен
            url = f"https://api.genius.com/search?q={query}"
            headers = {
                'Authorization': f'Bearer {GENIUS_ACCESS_TOKEN}'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Проверка на ошибки в ответе

            if response.status_code == 200:
                data = response.json()
                hits = data['response']['hits']
                if hits:
                    song = random.choice(hits)['result']
                    title = song['title']
                    artist = song['primary_artist']['name']
                    url = song['url']
                    await update.message.reply_text(f"Вот песня для тебя: {title} от {artist}\nПослушать можно здесь: {url}")
                else:
                    await update.message.reply_text("Не удалось найти песни.")
            else:
                await update.message.reply_text("Произошла ошибка при запросе к API.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching song from API: {e}")
            await update.message.reply_text("Произошла ошибка при обработке ответа от API.")
    elif text == '🌞 Пожелание':
        await update.message.reply_text('Желаю тебе прекрасного дня, полного радости и успехов!')
    elif text == '🌹 Показать розу':
        rose = random.choice(roses)
        await update.message.reply_text(f"Вот прекрасная роза для тебя: {rose}")
    elif text == '❓ Помощь':
        await help_command(update, context)
    else:
        await update.message.reply_text('Извини, я не понимаю. Пожалуйста, используй клавиатуру.')

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Regex('😊|🎵|🌞|🌹|❓'), handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
