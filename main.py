from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
from dotenv import load_dotenv
import os

# تحميل القيم من ملف .env
load_dotenv()

# التوكن الخاص بالبوت
BOT_TOKEN = os.getenv('BOT_TOKEN')

# مفتاح API الخاص بـ OMDb
OMDB_API_KEY = os.getenv('OMDB_API_KEY')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """إرسال رسالة ترحيبية عند بدء التفاعل مع البوت"""
    await update.message.reply_text('مرحباً! أنا بوت يتعرف على الأفلام والمسلسلات.')

async def get_movie_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """إرجاع معلومات الفيلم أو المسلسل"""
    movie_name = ' '.join(context.args)
    if not movie_name:
        await update.message.reply_text('يرجى إرسال اسم الفيلم أو المسلسل.')
        return
    
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data['Response'] == 'True':
        movie_info = f"اسم الفيلم: {data['Title']}\n"
        movie_info += f"السنة: {data['Year']}\n"
        movie_info += f"التقييم: {data['imdbRating']}\n"
        movie_info += f"النوع: {data['Genre']}\n"
        movie_info += f"الوصف: {data['Plot']}"
        await update.message.reply_text(movie_info)
    else:
        await update.message.reply_text(f"لم يتم العثور على فيلم باسم {movie_name}.")

async def main() -> None:
    """تشغيل البوت"""
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("movie", get_movie_info))

    # بدء تشغيل البوت
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
