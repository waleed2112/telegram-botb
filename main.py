from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes
import requests
from googletrans import Translator  # استيراد مكتبة الترجمة

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAGGv48BJqrzHJaUGWz4wQ2FL0iePS1HKxA'

# مفتاح API الخاص بـ OMDb
OMDB_API_KEY = 'aa7d3da9'

# دالة لترجمة القصة إلى العربية
def translate_to_arabic(text):
    translator = Translator()
    translated = translator.translate(text, src='en', dest='ar')
    return translated.text

# دالة لبدء التفاعل مع البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply("مرحبًا! أرسل لي اسم فيلم أو مسلسل لتحصل على تقييماته.")

# دالة لمعالجة النصوص التي تحتوي على أسماء الأفلام والمسلسلات
async def handle_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    movie_name = update.message.text
    await update.message.reply(f"جاري البحث عن فيلم {movie_name}...")

    # جلب بيانات الفيلم من OMDb API
    movie_url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}&plot=short&language=en"
    response = requests.get(movie_url)
    
    if response.status_code == 200:
        movie_data = response.json()
        if movie_data.get("Response") == "True":
            movie_title = movie_data.get("Title")
            movie_year = movie_data.get("Year")
            movie_plot = movie_data.get("Plot")
            
            # ترجمة القصة إلى العربية
            translated_plot = translate_to_arabic(movie_plot)
            
            # إرسال التقييمات والقصة
            await update.message.reply(f"اسم الفيلم: {movie_title}\nالسنة: {movie_year}\nالقصة: {translated_plot}")
        else:
            await update.message.reply("لم يتم العثور على معلومات الفيلم.")
    else:
        await update.message.reply("حدث خطأ أثناء جلب بيانات الفيلم.")

# دالة لتشغيل البوت
def main():
    # إنشاء التطبيق مع التوكن
    app = Application.builder().token(BOT_TOKEN).build()

    # إضافة معالجات الأوامر
    app.add_handler(MessageHandler(filters.TEXT, handle_movie))
    app.add_handler(CommandHandler("start", start))

    # بدء البوت
    app.run_polling()

if __name__ == '__main__':
    main()
