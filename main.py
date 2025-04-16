import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN, OMDB_API_KEY  # تأكد من استيراد التكوينات من ملف config.py

# دالة للتعامل مع الصور والفيديوهات
async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("استلمت الصورة أو الفيديو، جاري التحليل...")

    # جلب أول صورة أو فيديو من الرسالة
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        file = await context.bot.get_file(file_id)
        file_url = file.file_path
    elif update.message.video:
        file_id = update.message.video.file_id
        file = await context.bot.get_file(file_id)
        file_url = file.file_path
    else:
        return

    # هنا نرفع الصورة أو الفيديو إلى خدمة تحليل
    response = requests.post(
        'https://api.imagga.com/v2/tags',  # هنا نستخدم خدمة تحليل الصور
        data={'image_url': file_url},
        headers={'Authorization': 'Basic <Your API Key>'}  # ضع هنا مفتاح API
    )

    if response.status_code == 200:
        tags = response.json()['result']['tags']
        name = tags[0]['tag']  # استخدم أول وسم كاسم الفيلم أو المسلسل
        
        # الآن نبحث عن معلومات الفيلم باستخدام OMDb API
        omdb_response = requests.get(f"http://www.omdbapi.com/?t={name}&apikey={OMDB_API_KEY}")
        omdb_data = omdb_response.json()

        if omdb_data['Response'] == 'True':
            movie_info = f"اسم الفيلم: {omdb_data['Title']}\n" \
                         f"النوع: {omdb_data['Genre']}\n" \
                         f"سنة الإصدار: {omdb_data['Year']}\n" \
                         f"التقييم: {omdb_data['imdbRating']}\n" \
                         f"القصة: {omdb_data['Plot']}"
            await update.message.reply_text(movie_info)
        else:
            await update.message.reply_text("لم أتمكن من العثور على معلومات الفيلم.")
    else:
        await update.message.reply_text("حدث خطأ أثناء تحليل الصورة أو الفيديو.")

# دالة لبدء التفاعل مع البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply("مرحبًا! أنا هنا للمساعدة في التعرف على الأفلام والمسلسلات.")

# دالة لتشغيل البوت
def main():
    # بناء التطبيق باستخدام التوكن
    app = Application.builder().token(BOT_TOKEN).build()

    # إضافة معالجات الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, handle_media))

    # بدء البوت
    app.run_polling()

if __name__ == '__main__':
    main()
