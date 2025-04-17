import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests
import pytz
import nest_asyncio

# تطبيق nest_asyncio
nest_asyncio.apply()

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAGGv48BJqrzHJaUGWz4wQ2FL0iePS1HKxA'

# مفتاح API الخاص بـ OMDb
OMDB_API_KEY = 'aa7d3da9'

# تعيين المنطقة الزمنية
timezone = pytz.timezone("Asia/Riyadh")

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
        # استخراج البيانات من الاستجابة
        title = data.get('Title')
        year = data.get('Year')
        rated = data.get('Rated')
        genre = data.get('Genre')
        imdb_rating = data.get('imdbRating')
        plot = data.get('Plot')
        poster_url = data.get('Poster')

        # إرسال المعلومات للمستخدم
        movie_details = f"اسم الفيلم/المسلسل: {title}\n" \
                        f"السنة: {year}\n" \
                        f"التصنيف: {rated}\n" \
                        f"النوع: {genre}\n" \
                        f"التقييم: {imdb_rating}\n" \
                        f"الملخص: {plot}"

        # إرسال النص
        await update.message.reply_text(movie_details)

        # إرسال الصورة إذا كانت موجودة
        if poster_url and poster_url != 'N/A':
            await update.message.reply_photo(poster_url)

    else:
        await update.message.reply_text("لم أتمكن من العثور على معلومات للفيلم أو المسلسل الذي أرسلته.")

# دالة لمعالجة الأخطاء
def error(update: Update, context: CallbackContext) -> None:
    logger.warning('قُوبل خطأ "%s" من قبل "%s"', context.error, update)

# الوظيفة الرئيسية لإعداد البوت
async def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # إضافة معالج للأمر /start
