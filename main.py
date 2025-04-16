from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes
from google.cloud import vision
from google.cloud.vision import ImageAnnotatorClient
import os
import requests

# تعيين مفتاح Google Cloud API (يجب أن تكون قد قمت بتعيين ملف البيئة GOOGLE_APPLICATION_CREDENTIALS)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_google_credentials.json"

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAGGv48BJqrzHJaUGWz4wQ2FL0iePS1HKxA'

# مفتاح OMDb API لتحليل الصور والفيديوهات
OMDB_API_KEY = 'aa7d3da9'

# دالة لبدء التفاعل مع البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply("مرحبًا! أرسل لي صورة أو فيديو لتحليل اسم الفيلم.")

# دالة لتحليل الصورة باستخدام Google Cloud Vision API
async def analyze_image(image_path: str) -> str:
    client = ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)

    labels = response.label_annotations
    descriptions = [label.description for label in labels]
    return ", ".join(descriptions)

# دالة لمعالجة الصور والفيديوهات
async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.photo or update.message.video:
        await update.message.reply("استلمت الصورة أو الفيديو، وجاري التحليل...")

        # جلب الصورة أو الفيديو من الرسالة
        file_id = update.message.photo[-1].file_id if update.message.photo else update.message.video.file_id
        file = await context.bot.get_file(file_id)
        file_url = file.file_path
        
        # حفظ الصورة مؤقتًا لتحليلها باستخدام Google Vision API
        image_path = "temp_image.jpg"
        await file.download_to_drive(image_path)

        # تحليل الصورة باستخدام Google Vision API
        labels = await analyze_image(image_path)

        # إرسال النتائج للمستخدم
        await update.message.reply(f"تم العثور على التصنيفات التالية: {labels}")
        
        # حذف الصورة المؤقتة
        os.remove(image_path)
    else:
        await update.message.reply("لم أتمكن من التعرف على صورة أو فيديو.")

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
