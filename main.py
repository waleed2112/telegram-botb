from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import requests
import os

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAGGv48BJqrzHJaUGWz4wQ2FL0iePS1HKxA'

# مفتاح OMDb API لتحليل الصور والفيديوهات
OMDB_API_KEY = 'aa7d3da9'

# دالة لبدء التفاعل مع البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply("مرحبًا! أرسل لي صورة أو فيديو لتحليل اسم الفيلم.")

# دالة لمعالجة الصور والفيديوهات
async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.photo or update.message.video:
        await update.message.reply("استلمت الصورة أو الفيديو، وجاري التحليل...")

        # جلب الصورة أو الفيديو من الرسالة
        file_id = update.message.photo[-1].file_id if update.message.photo else update.message.video.file_id
        file = await context.bot.get_file(file_id)
        file_url = file.file_path
        
        # هنا يمكنك إرسال الطلب لـ OMDb API لتحليل الفيلم
        movie_url = f"http://www.omdbapi.com/?t={file_url}&apikey={OMDB_API_KEY}"
        
        response = requests.get(movie_url)
        
        # إذا تم العثور على معلومات الفيلم
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
