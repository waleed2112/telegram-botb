from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import requests
from google.cloud import vision
from google.cloud.vision import types

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAGGv48BJqrzHJaUGWz4wQ2FL0iePS1HKxA'

# مفتاح OMDb API لتحليل الأفلام
OMDB_API_KEY = 'aa7d3da9'

# مفتاح Google Cloud Vision API
VISION_API_KEY = 'AIzaSyDu_X_jlDgyBZUOxmr5tbOkPjVukMk45Ug'

# إعدادات Google Vision API (يجب أن يكون لديك ملف JSON للمفتاح)
vision_client = vision.ImageAnnotatorClient(credentials=VISION_API_KEY)

# دالة لبدء التفاعل مع البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply("مرحبًا! أرسل لي صورة أو فيديو لتحليل اسم الفيلم.")

# دالة لتحليل النصوص في الصور باستخدام Google Vision API
async def analyze_image(image_url: str) -> str:
    """تحليل الصورة واستخراج النصوص باستخدام Google Vision API"""
    # تنزيل الصورة من الإنترنت
    image = vision.Image()
    image.source.image_uri = image_url

    # إرسال الصورة إلى Google Vision API للحصول على النصوص
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description.strip()  # الحصول على أول نص مكتشف من الصورة
    else:
        return ""

# دالة لمعالجة الصور والفيديوهات
async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.photo or update.message.video:
        await update.message.reply("استلمت الصورة أو الفيديو، وجاري التحليل...")

        # جلب الصورة أو الفيديو من الرسالة
        file_id = update.message.photo[-1].file_id if update.message.photo else update.message.video.file_id
        file = await context.bot.get_file(file_id)
        file_url = file.file_path

        # هنا نستخدم Google Vision API لتحليل النصوص
        movie_name = await analyze_image(file_url)

        if movie_name:
            # استدعاء OMDb API للحصول على معلومات الفيلم
            movie_url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
            response = requests.get(movie_url)

            if response.status_code == 200:
                movie_data = response.json()
                if movie_data.get("Response") == "True":
                    movie_name = movie_data.get("Title")
                    movie_year = movie_data.get("Year")
                    movie_plot = movie_data.get("Plot")
                    await update.message.reply(f"اسم الفيلم: {movie_name}\nالسنة: {movie_year}\nالقصة: {movie_plot}")
                else:
                    await update.message.reply("لم يتم العثور على معلومات الفيلم.")
            else:
                await update.message.reply("حدث خطأ أثناء معالجة الصورة أو الفيديو.")
        else:
            await update.message.reply("لم أتمكن من استخراج اسم الفيلم من الصورة.")

# دالة لتشغيل البوت
def main():
    # إنشاء التطبيق مع التوكن
    app = Application.builder().token(BOT_TOKEN).build()

    # إضافة معالجات الأوامر
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, handle_media))
    app.add_handler(CommandHandler("start", start))

    # بدء البوت
    app.run_polling()

if __name__ == '__main__':
    main()
