import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAGGv48BJqrzHJaUGWz4wQ2FL0iePS1HKxA'

# مفتاح API الخاص بـ OMDb
OMDB_API_KEY = 'aa7d3da9'

# إعدادات اللوج
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# دالة لجلب تقييم الفيلم باستخدام OMDb API
def get_movie_rating(movie_name):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get("Response") == "True":
        return data.get("imdbRating")
    return "Movie not found."

# دالة لمعالجة الأمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Send me a movie name to get its IMDb rating.')

# دالة لمعالجة الأمر /movie
async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_name = ' '.join(context.args)
    if movie_name:
        rating = get_movie_rating(movie_name)
        await update.message.reply_text(f"IMDb Rating for {movie_name}: {rating}")
    else:
        await update.message.reply_text('Please provide a movie name after the command.')

# دالة رئيسية لتشغيل البوت
async def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # إضافة المعالجات للأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("movie", movie))

    # بدء البوت
    await application.run_polling()

# تشغيل البوت
if __name__ == '__main__':
    asyncio.run(main())
