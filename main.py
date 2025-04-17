import logging
import asyncio
import pytz
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.util import astimezone

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAGGv48BJqrzHJaUGWz4wQ2FL0iePS1HKxA'

# مفتاح API الخاص بـ OMDb
OMDB_API_KEY = 'aa7d3da9'

# تحديد المنطقة الزمنية
timezone = pytz.timezone("Asia/Riyadh")  # اختر المنطقة الزمنية التي تناسبك

# إعداد الـ scheduler باستخدام المنطقة الزمنية
scheduler = AsyncIOScheduler(timezone=timezone)
scheduler.start()

# إعداد التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# دالة بدء البوت
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('مرحبًا! أنا بوت لتحليل الأفلام والأنمي.')

# دالة الحصول على معلومات الفيلم أو المسلسل
async def get_movie_info(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("من فضلك أدخل اسم الفيلم أو المسلسل بعد الأمر.")
        return

    # استخدم OMDb API للحصول على معلومات الفيلم
    url = f"http://www.om
