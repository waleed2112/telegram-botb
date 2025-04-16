from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
import requests
from config import BOT_TOKEN, OMDB_API_KEY  # ✅ جلب التوكن والمفتاح من config.py

# دالة بدء التفاعل مع البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل لي اسم فيلم أو مسلسل 📽️، وأرجع لك تقييمه 🎯")

# دالة لمعالجة رسائل المستخدم
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    url = f"http://www.omdbapi.com/?t={query}&apikey={OMDB_API_KEY}"

    response = requests.get(url)
    data = response.json()

    if data.get("Response") == "True":
        title = data.get("Title", "غير معروف")
        year = data.get("Year", "غير معروف")
        rating = data.get("imdbRating", "غير متوفر")
        plot = data.get("Plot", "لا توجد نبذة.")

        reply = f"🎬 *{title}*\n📅 السنة: {year}\n⭐ التقييم: {rating}/10\n📝 القصة: {plot}"
    else:
        reply = "❌ لم أتمكن من العثور على الفيلم أو المسلسل. تأكد من الاسم."

    await update.message.reply_text(reply)

# تشغيل البوت
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
