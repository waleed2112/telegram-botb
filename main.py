import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAGGv48BJqrzHJaUGWz4wQ2FL0iePS1HKxA'

# مفتاح API الخاص بـ OMDb
OMDB_API_KEY = 'aa7d3da9'

# تفعيل التسجيل لعرض الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# دالة بدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('مرحبًا! أنا بوت يمكنني مساعدتك في العثور على تفاصيل الأفلام.')

# دالة لتحليل تفاصيل الفيلم
async def fetch_movie_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        movie_name = ' '.join(context.args)
        url = f'http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}'
        response = requests.get(url)
        data = response.json()

        if data.get("Response") == "True":
            movie_info = (
                f"اسم الفيلم: {data['Title']}\n"
                f"السنة: {data['Year']}\n"
                f"التقييم: {data['imdbRating']}\n"
                f"القصة: {data['Plot']}\n"
            )
            await update.message.reply_text(movie_info)
        else:
            await update.message.reply_text("عذرًا، لم أتمكن من العثور على الفيلم.")
    else:
        await update.message.reply_text("من فضلك، قدم اسم الفيلم بعد الأمر.")

# دالة لتشغيل البوت
async def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    # إضافة معالج للرد على الأمر /start
    application.add_handler(CommandHandler("start", start))

    # إضافة معالج لتحليل الأفلام باستخدام OMDb API
    application.add_handler(CommandHandler("movie", fetch_movie_details))

    # بدء البوت
    await application.run_polling()

if __name__ == '__main__':
    import
