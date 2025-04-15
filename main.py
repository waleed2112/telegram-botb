from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN, API_KEY

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("استلمت الصورة أو الفيديو، وجاري التحليل...")
    # هنا تقدر ترسل الصورة أو الفيديو لمزود الخدمة باستخدام API_KEY
    # وترجع النتيجة للمستخدم

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
