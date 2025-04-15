from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN, API_KEY  # تأكد من استيراد التكوينات من ملف config.py

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("استلمت الصورة أو الفيديو، وجاري التحليل...")
    # هنا تقدر ترسل الصورة أو الفيديو لمزود الخدمة باستخدام API_KEY
    # وترجع النتيجة للمستخدم

def main():
    # بناء التطبيق باستخدام التوكن من ملف التكوين
    app = Application.builder().token(BOT_TOKEN).build()

    # إضافة معالج الصور والفيديوهات
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, handle_message))

    # بدء البوت
    app.run_polling()

if __name__ == "__main__":
    main()
