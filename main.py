import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Application
import requests
import os
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAGGv48BJqrzHJaUGWz4wQ2FL0iePS1HKxA'

# مفتاح API الخاص بـ OMDb
OMDB_API_KEY = 'aa7d3da9'

# تعيين المنطقة الزمنية
timezone = pytz.timezone("Asia/Riyadh")  # اختر المنطقة الزمنية المناسبة

# إعدادات التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# دالة لمعالجة الأمر /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('مرحباً! أرسل اسم الفيلم أو المسلسل للحصول على التقييم.')

# دالة لمعالجة الطلبات المرتبطة بالأفلام أو المسلسلات
async def movie_info(update: Update, context: CallbackContext) -> None:
    movie_name = ' '.join(context.args)
    if not movie_name:
        await update.message.reply_text("يرجى إدخال اسم الفيلم أو المسلسل بعد الأمر.")
        return

    # الاتصال بـ OMDb API للحصول على معلومات الفيلم أو المسلسل
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data.get("Response") == "True":
        # إرسال المعلومات للمستخدم
        movie_details = f"اسم الفيلم/المسلسل: {data.get('Title')}\n" \
                        f"السنة: {data.get('Year')}\n" \
                        f"التصنيف: {data.get('Rated')}\n" \
                        f"النوع: {data.get('Genre')}\n" \
                        f"التقييم: {data.get('imdbRating')}\n" \
                        f"الملخص: {data.get('Plot')}"
        await update.message.reply_text(movie_details)
    else:
        await update.message.reply_text("لم أتمكن من العثور على معلومات للفيلم أو المسلسل الذي أرسلته.")

# دالة لمعالجة الأخطاء
def error(update: Update, context: CallbackContext) -> None:
    logger.warning('قُوبل خطأ "%s" من قبل "%s"', context.error, update)

# الوظيفة الرئيسية لإعداد البوت
async def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # إضافة معالج للأمر /start
    application.add_handler(CommandHandler("start", start))

    # إضافة معالج للأمر الذي يتعامل مع الفيلم أو المسلسل
    application.add_handler(CommandHandler("movie", movie_info))

    # إضافة معالج للأخطاء
    application.add_error_handler(error)

    # بدء تشغيل البوت
    await application.run_polling()

# تشغيل البوت مباشرة باستخدام run_polling
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
