from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import os

BOT_TOKEN = 'توكن البوت هنا'
OMDB_API_KEY = 'مفتاح OMDb API هنا'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! أرسل لي اسم فيلم أو مسلسل وسأعطيك التقييمات 🔍🎬")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    url = f"http://www.omdbapi.com/?t={query}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data.get("Response") == "True":
        title = data.get("Title")
        year = data.get("Year")
        imdb = data.get("imdbRating")
        plot = data.get("Plot")
        await update.message.reply_text(f"🎬 {title} ({year})\n⭐ IMDB: {imdb}\n📝 القصة: {plot}")
    else:
        await update.message.reply_text("لم يتم العثور على نتائج 😔")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
