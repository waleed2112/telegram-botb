from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import requests

# ============ التكوين ============
BOT_TOKEN = '7614704758:AAGGv48BJqrzHJaUGWz4wQ2FL0iePS1HKxA'
OMDB_API_KEY = 'aa7d3da9'
# =================================

# عند بدء المحادثة مع البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("مرحبًا! أرسل لي اسم أي فيلم أو مسلسل وسأعطيك التقييم 📽️⭐")

# عند إرسال أي رسالة نصية (اسم فيلم أو مسلسل)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.message.text.strip()
    await update.message.reply_text("جاري البحث عن التقييم... 🔍")

    url = f"http://www.omdbapi.com/?t={query}&apikey={OMDB_API_KEY}&plot=short&language=ar"
    response = requests.get(url)
    data = response.json()

    if data.get("Response") == "True":
        title = data.get("Title")
        year = data.get("Year")
        rating = data.get("imdbRating")
        plot = data.get("Plot")
        poster_url = data.get("Poster")  # رابط الصورة
        
        # الرد بالنص والصورة
        reply = f"🎬 *الاسم:* {title}\n📅 *السنة:* {year}\n⭐ *التقييم:* {rating}\n📝 *القصة:* {plot}"
        await update.message.reply_markdown(reply)
        
        if poster_url != "N/A":
            # إرسال الصورة إذا كانت موجودة
            await update.message.reply_photo(poster_url)
    else:
        await update.message.reply_text("لم أتمكن من العثور على هذا الفيلم أو المسلسل 😕")

# تشغيل البوت
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ البوت شغال... انتظر الرسائل.")
    app.run_polling()

if __name__ == '__main__':
    main()
