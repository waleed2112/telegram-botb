import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.ext import MessageHandler, filters
import asyncio

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAGGv48BJqrzHJaUGWz4wQ2FL0iePS1HKxA'

# مفتاح API الخاص بـ OMDb
OMDB_API_KEY = 'aa7d3da9'

# إعدادات تسجيل الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# دالة للتعامل مع الأمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply(f"مرحبًا {user.first_name}! أنا بوت تلغرام يمكنني مساعدتك في العثور على معلومات حول الأفلام والمسلسلات.")

# دالة للتعامل مع تحليل الأفلام باستخدام OMDb API
async def fetch_movie_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    movie_name = ' '.join(context.args)
    
    if not movie_name:
        await update.message.reply("من فضلك، أرسل اسم الفيلم أو المسلسل الذي تريد معرفة تفاصيله.")
        return
    
    # إرسال طلب إلى OMDb API
    response = requests.get(f'http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}')
    data = response.json()

    if data.get('Response') == 'True':
        # عرض تفاصيل الفيلم أو المسلسل
        title = data.get('Title')
        year = data.get('Year')
        genre = data.get('Genre')
        plot = data.get('Plot')
        rating = data.get('imdbRating')

        await update.message.reply(f"🎬 {title} ({year})\n"
                                   f"النوع: {genre}\n"
                                   f"التقييم: {rating}/10\n"
                                   f"القصة: {plot}")
    else:
        await update.message.reply(f"لم أتمكن من العثور على معلومات حول {movie_name}. حاول اسم مختلف.")

# الدالة الرئيسية لبدء البوت
async def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    # إضافة معالج للرد على الأمر /start
    application.add_handler(CommandHandler_
